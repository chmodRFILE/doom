// Utility functions for weapon system

// Calculate damage based on distance
export const calculateDamage = (baseDamage, distance, maxRange) => {
  if (distance > maxRange) return 0;
  
  // Simple linear falloff
  const ratio = 1 - (distance / maxRange);
  return Math.max(0, baseDamage * ratio);
};

// Check if weapon can hit target
export const canHitTarget = (weapon, targetDistance) => {
  return targetDistance <= weapon.range;
};

// Get weapon type based on name
export const getWeaponType = (weaponName) => {
  const types = {
    pistol: 'handgun',
    rifle: 'assault',
    shotgun: 'shotgun'
  };
  
  return types[weaponName] || 'unknown';
};

// Format weapon stats for display
export const formatWeaponStats = (weapon) => {
  return {
    name: weapon.name,
    damage: `${weapon.damage} DMG`,
    range: `${weapon.range}m`,
    fireRate: `${weapon.fireRate} RPM`,
    ammo: `${weapon.ammo}/${weapon.maxAmmo}`
  };
};

// Weapon cooldown timer
export class WeaponCooldown {
  constructor(duration) {
    this.duration = duration;
    this.startTime = null;
    this.isReady = true;
  }

  start() {
    this.startTime = Date.now();
    this.isReady = false;
    
    setTimeout(() => {
      this.isReady = true;
    }, this.duration);
  }

  isOnCooldown() {
    return !this.isReady;
  }

  getRemainingTime() {
    if (this.isReady) return 0;
    const elapsed = Date.now() - this.startTime;
    return Math.max(0, this.duration - elapsed);
  }
}