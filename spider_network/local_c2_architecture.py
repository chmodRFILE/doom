# Local C2 Architecture for Doom Spider Network
# Minimal Container Approach - 99% Local System
#
# This module implements a local-first C2 architecture where instead of
# routing and managing remote C2 bots, we create minimal containers with
# Spider-specific data and let scripts sleep for calculated times.

"""Local C2 Architecture for Doom Spider Network

This module implements a local-first C2 architecture where instead of
routing and managing remote C2 bots, we create minimal containers with
Spider-specific data and let scripts sleep for calculated times.

Key Components:
  - LocalContainer: Creates and manages minimal ~50Mb containers
  - SleepScheduler: Scripts that sleep for calculated durations
  - KeyManagement: Handles key refusal and countdown logic
  - ContainerLifecycle: Drop salt, wipe container, flag host on failure

"""

import json
import os
import subprocess
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import existing XOR architecture components
from spider_network.xor_architecture import XORSaltingEncryption, XORKeyRing, XORRollArchitecture


class LocalContainer:
    """Creates and manages minimal ~50Mb containers for C2 communication.

    Each container holds:
    - target: Target domain/information
    - timestamp: Creation/activation timestamp
    - approximated return of Salted_Spider: Encrypted spider data
    - salt: XOR salt for decryption
    - container_id: Unique identifier
    """

    def __init__(self, container_dir: str = "storage/local_containers", keyring=None):
        """Initialize local container manager.

        Args:
            container_dir (str): Directory to store container data
            keyring (XORKeyRing): Keyring for encryption/decryption
        """
        self.container_dir = Path(container_dir)
        self.container_dir.mkdir(parents=True, exist_ok=True)
        self.keyring = keyring or XORKeyRing()
        self.encryption = XORSaltingEncryption(self.keyring)
        self.lock = threading.Lock()

    def create_container(self, target: str, spider_data: Dict[str, Any],
                         salt: Optional[str] = None,
                         duration_seconds: int = 300) -> Dict[str, Any]:
        """Create a minimal container with Spider-specific data.

        Args:
            target (str): Target domain/information
            spider_data (Dict): Spider-specific data to store
            salt (Optional[str]): XOR salt for encryption
            duration_seconds (int): How long container should remain active (seconds)

        Returns:
            Dict: Container metadata including path and encrypted data
        """
        try:
            with self.lock:
                # Generate salt if not provided
                if not salt:
                    salt = self.encryption.generate_salt()

                # Create container ID
                container_id = f"container_{int(time.time())}_{hash(target) % 10000}"

                # Create timestamp
                timestamp = datetime.now().isoformat()

                # Approximate return of Salted_Spider - encrypt the spider data
                encrypted_data = self.encryption.encrypt_command(
                    {"target": target, "data": spider_data, "timestamp": timestamp},
                    container_id)

                # Container metadata
                container_info = {
                    "container_id": container_id,
                    "target": target,
                    "timestamp": timestamp,
                    "encrypted_data": encrypted_data,
                    "salt": salt,
                    "duration_seconds": duration_seconds,
                    "created_at": datetime.now().isoformat(),
                    "status": "active",
                    "file_size_mb": 0  # Will be updated after creation
                }

                # Write container to file (minimal size - just metadata + encrypted data)
                container_path = self.container_dir / f"{container_id}.json"
                with open(container_path, 'w') as f:
                    json.dump(container_info, f)

                # Update file size
                file_size = container_path.stat().st_size / (1024 * 1024)  # MB
                container_info["file_size_mb"] = round(file_size, 2)

                # Save updated container info
                with open(container_path, 'w') as f:
                    json.dump(container_info, f, indent=2)

                logger.info(f"Created container {container_id} ({file_size:.2f}MB) for target: {target}")
                return container_info
        except Exception as e:
            logger.error(f"Error creating container: {e}")
            raise


class SleepScheduler:
    """Manages scripts that sleep for calculated durations based on container data.

    The sleep duration is calculated based on:
    - Container creation timestamp
    - Approximated return data
    - Target-specific timing
    """

    def __init__(self, container: LocalContainer):
        """Initialize sleep scheduler.

        Args:
            container (LocalContainer): Container to schedule sleep for
        """
        self.container = container
        self.sleep_thread = None
        self.stop_event = threading.Event()

    def calculate_sleep_duration(self, target_timestamp: str, current_time: Optional[float] = None) -> float:
        """Calculate sleep duration based on container timestamp.

        Args:
            target_timestamp (str): ISO format timestamp from container
            current_time (Optional[float]): Current time in seconds

        Returns:
            float: Calculated sleep duration in seconds
        """
        try:
            if current_time is None:
                current_time = time.time()

            # Parse the target timestamp
            target_dt = datetime.fromisoformat(target_timestamp)
            current_dt = datetime.fromtimestamp(current_time)

            # Calculate elapsed time since container creation
            elapsed = (current_dt - target_dt).total_seconds()

            # Return remaining time if within duration, else 0
            # This creates the countdown effect
            # For this local architecture, we want a max of ~500 seconds (8min)
            max_duration = 500  # ~8 minutes, keeps things local and fast

            if elapsed < 0:
                # Container hasn't been created yet or timestamp is in future
                return abs(elapsed) % max_duration

            elapsed_mod = elapsed % max_duration

            # Return remaining time in the current cycle
            remaining = max_duration - elapsed_mod

            # Cap at max for the sleep command
            return min(remaining, float(max_duration))
        except Exception as e:
            logger.error(f"Error calculating sleep duration: {e}")
            return 300  # Default 5 minutes

    def start_sleep(self, container_id: str, sleep_duration: float) -> threading.Thread:
        """Start a sleep thread for the container.

        Args:
            container_id (str): Container identifier
            sleep_duration (float): Duration to sleep in seconds

        Returns:
            threading.Thread: Sleep thread instance
        """
        self.stop_event = threading.Event()

        def sleep_loop():
            """Internal sleep loop that handles countdown and checks."""
            logger.info(f"Sleep thread started for container {container_id}")
            logger.info(f"Sleep duration: {sleep_duration:.3f} seconds")

            # Sleep in small increments to allow interruption/checks
            increment = 0.01  # 10ms increments
            remaining = sleep_duration

            while remaining > 0 and not self.stop_event.is_set():
                # Sleep in small increment
                sleep_time = min(increment, remaining)
                time.sleep(sleep_time)
                remaining -= sleep_time

                # Check if we should stop
                if self.stop_event.is_set():
                    logger.info(f"Sleep stopped early for container {container_id}")
                    return

            # Countdown complete - trigger sync check
            logger.info(f"Countdown complete for container {container_id}")
            self.container.trigger_sync_check(container_id)

        self.sleep_thread = threading.Thread(target=sleep_loop, daemon=True)
        self.sleep_thread.start()
        return self.sleep_thread


class KeyManagement:
    """Handles key refusal and countdown logic for the local C2 system.

    When a key is 'refused' (not available/authorized),
    the system waits for the countdown to reach 0.000 before attempting sync.
    """

    def __init__(self, keyring, container: LocalContainer):
        """Initialize key management.

        Args:
            keyring (XORKeyRing): Keyring for encryption/decryption
            container (LocalContainer): Container manager
        """
        self.keyring = keyring
        self.container = container
        self.refusal_count = 0
        self.max_refusals = 3

    def mark_key_refused(self, container_id: str) -> Dict[str, Any]:
        """Mark a key as refused for a container.

        Args:
            container_id (str): Container identifier

        Returns:
            Dict: Status of the key refusal
        """
        with self.container.lock:
            self.refusal_count += 1
            logger.warning(f"Key refused for container {container_id} (refusal #{self.refusal_count})")

            # Check if we've reached max refusals
            if self.refusal_count >= self.max_refusals:
                logger.error(f"Max refusals reached for container {container_id}")
                return {
                    "status": "key_permanently_refused",
                    "container_id": container_id,
                    "refusal_count": self.refusal_count,
                    "action": "drop_salt_wipe_container"
                }

            return {
                "status": "key_refused",
                "container_id": container_id,
                "refusal_count": self.refusal_count,
                "remaining_refusals": self.max_refusals - self.refusal_count
            }

    def check_key_authorized(self, container_id: str) -> bool:
        """Check if the key is authorized/available for a container.

        Args:
            container_id (str): Container identifier

        Returns:
            bool: True if key is authorized, False if refused
        """
        # In a real implementation, this would check key authorization
        # For local architecture, we check keyring status
        key_data = self.keyring.get_key(container_id)
        if key_data and key_data.get('status') == 'active':
            return True
        return False


class ContainerLifecycle:
    """Handles container lifecycle events including cleanup and host flagging.

    On failure scenarios:
    1. Drop the salt (remove encryption salt)
    2. Wipe the container (remove container data)
    3. Flag the host as isolated/offline
    """

    FLAG_PATTERN = "flag_isolated"  # Pattern that could match various flag systems

    def __init__(self, container: LocalContainer, key_mgmt: KeyManagement):
        """Initialize container lifecycle manager.

        Args:
            container (LocalContainer): Container manager
            key_mgmt (KeyManagement): Key management system
        """
        self.container = container
        self.key_mgmt = key_mgmt

    def handle_key_refusal(self, container_id: str) -> Dict[str, Any]:
        """Handle key refusal event with appropriate actions.

        Args:
            container_id (str): Container identifier

        Returns:
            Dict: Actions taken
        """
        refusal_result = self.key_mgmt.mark_key_refused(container_id)

        if refusal_result["status"] == "key_permanently_refused":
            # Both failed - drop salt, wipe container, flag host
            return self._cleanup_container(container_id, force=True)

        return refusal_result

    def _cleanup_container(self, container_id: str, force: bool = False) -> Dict[str, Any]:
        """Drop salt, wipe container, and flag the host.

        Args:
            container_id (str): Container identifier
            force (bool): Force cleanup even if not in refusal state

        Returns:
            Dict: Cleanup actions and results
        """
        try:
            with self.container.lock:
                # Get container info before cleanup
                container_path = self.container.container_dir / f"{container_id}.json"

                if container_path.exists():
                    with open(container_path, 'r') as f:
                        container_info = json.load(f)

                    logger.info(f"Cleaning up container {container_id}")

                    # Step 1: Drop the salt (remove encryption salt)
                    # This makes the encrypted data undecryptable
                    container_info["salt_dropped"] = True
                    container_info["salt"] = None

                    # Step 2: Wipe the container (remove container data)
                    container_path.unlink()  # Remove the file
                    logger.info(f"Wiped container file: {container_path}")

                    # Step 3: Flag the host as isolated
                    # The flag pattern is "flag_isolated" - can match various systems
                    host_flag = {
                        "host_flag": self.FLAG_PATTERN,
                        "container_id": container_id,
                        "timestamp": datetime.now().isoformat(),
                        "reason": "key_refusal_or_failure",
                        "action_taken": "drop_salt_wipe_container"
                    }

                    # Write flag file alongside container
                    flag_path = self.container.container_dir / f"{container_id}.flag"
                    with open(flag_path, 'w') as f:
                        json.dump(host_flag, f)
                    logger.info(f"Host flagged as isolated: {host_flag}")

                    return {
                        "status": "container_cleaned_up",
                        "container_id": container_id,
                        "salt_dropped": True,
                        "container_wiped": True,
                        "host_flagged": True,
                        "flag_pattern": self.FLAG_PATTERN,
                        "flag_details": host_flag
                    }

                logger.warning(f"Container {container_id} not found for cleanup")
                return {
                    "status": "container_not_found",
                    "container_id": container_id
                }
        except Exception as e:
            logger.error(f"Error during container cleanup: {e}")
            raise


class LocalC2System:
    """Main Local C2 System that orchestrates the local-first architecture.

    This system:
    - Creates minimal ~50Mb containers with Spider-specific data
    - Uses SleepScheduler for countdown-based sync
    - Manages key refusal and countdown logic
    - Handles container lifecycle on failures
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the local C2 system.

        Args:
            config (Optional[Dict]): Configuration options
        """
        self.config = config or {}
        self.keyring = XORKeyRing(self.config.get('keyring_path', 'storage/keyring.json'))
        self.container_mgr = LocalContainer(
            self.config.get('container_dir', 'storage/local_containers'),
            self.keyring
        )
        self.key_mgmt = KeyManagement(self.keyring, self.container_mgr)
        self.lifecycle = ContainerLifecycle(self.container_mgr, self.key_mgmt)

        # Integration with existing XOR roll architecture
        self.roll_arch = XORRollArchitecture(self.keyring)

    def create_and_schedule(self, target: str, spider_data: Dict[str, Any],
                            duration_seconds: int = 300) -> Dict[str, Any]:
        """Create a local container and schedule sleep-based sync.

        Args:
            target (str): Target domain/information
            spider_data (Dict): Spider-specific data
            duration_seconds (int): Container active duration

        Returns:
            Dict: Result with container info and sleep scheduler
        """
        try:
            # Step 1: Create the minimal container
            container_info = self.container_mgr.create_container(
                target=target,
                spider_data=spider_data,
                duration_seconds=duration_seconds
            )
            container_id = container_info["container_id"]

            # Step 2: Initialize sleep scheduler
            sleep_scheduler = SleepScheduler(self.container_mgr)

            # Step 3: Calculate sleep duration
            target_timestamp = container_info["timestamp"]
            sleep_duration = sleep_scheduler.calculate_sleep_duration(target_timestamp)

            # Step 4: Start the sleep thread
            sleep_thread = sleep_scheduler.start_sleep(container_id, sleep_duration)

            # Step 5: Return result with all info
            result = {
                "status": "container_created_and_scheduled",
                "container_id": container_id,
                "target": target,
                "container_info": container_info,
                "sleep_duration": sleep_duration,
                "sleep_thread_active": sleep_thread.is_alive() if sleep_thread else False,
                "key_mgmt": self.key_mgmt,
                "lifecycle": self.lifecycle
            }

            logger.info(f"Local C2 system: Created container {container_id} with {sleep_duration:.2f}s sleep schedule")
            return result
        except Exception as e:
            logger.error(f"Error creating/scheduling local C2: {e}")
            raise

    def handle_container_event(self, container_id: str, event: str) -> Dict[str, Any]:
        """Handle events for a container (key refusal, timeout, etc.).

        Args:
            container_id (str): Container identifier
            event (str): Event type ("key_refused", "timeout", "success")

        Returns:
            Dict: Result of event handling
        """
        try:
            if event == "key_refused":
                return self.lifecycle.handle_key_refusal(container_id)

            elif event == "timeout":
                # Timeout reached without key authorization
                logger.warning(f"Timeout reached for container {container_id}")
                return self.lifecycle._cleanup_container(container_id, force=True)

            elif event == "success":
                # Sync successful - could renew or flag as healthy
                logger.info(f"Sync successful for container {container_id}")
                return {"status": "sync_successful", "container_id": container_id}

            else:
                logger.error(f"Unknown event: {event}")
                return {"status": "error", "message": f"Unknown event: {event}"}
        except Exception as e:
            logger.error(f"Error handling container event: {e}")
            raise


def example_local_c2_usage():
    """Example usage of the local C2 system.

    This demonstrates the 99% local architecture:
    1. Create minimal container with spider data
    2. Sleep for calculated duration
    3. Attempt sync when countdown reaches 0.000
    4. On failure: drop salt, wipe container, flag host as isolated
    """
    print("=" * 70)
    print("Local C2 Architecture - 99% Local System")
    print("=" * 70)

    # Initialize the local C2 system
    local_c2 = LocalC2System()

    # Example spider data
    spider_data = {
        "target": "example-doom-site.com",
        "timestamp": datetime.now().isoformat(),
        "approximated_return": "salted_spider_estimate"
    }

    # Create container and schedule sleep
    result = local_c2.create_and_schedule(
        target="example-doom-site.com",
        spider_data=spider_data,
        duration_seconds=300  # 5 minutes max
    )

    print(f"\nContainer ID: {result['container_id']}")
    print(f"Target: {result['container_info']['target']}")
    print(f"Sleep duration: {result['sleep_duration']:.3f} seconds")
    print(f"Container size: {result['container_info']['file_size_mb']} MB")
    print(f"Sleep thread active: {result['sleep_thread_active']}")

    print("\n--- Countdown in progress ---")
    print("The script will sleep and then attempt sync when countdown reaches 0.000")
    print("If key is refused during countdown...")
    print("  - After 3 refusals: key permanently refused")
    print("  - On final refusal: drop salt, wipe container, flag host as isolated")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_local_c2_usage()