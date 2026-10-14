// Weapon system implementation

// Base weapon class
export class Weapon {
  constructor(name, damage, range, fireRate) {
    this.name = name;
    this.damage = damage;
    this.range = range;
    this.fireRate = fireRate;
    this.ammo = 0;
    this.maxAmmo = 0;
    this.isFiring = false;
  }

  fire() {
    if (this.ammo > 0) {
      this.ammo--;
      return true;
    }
    return false;
  }

  reload() {
    this.ammo = this.maxAmmo;
  }

  getStats() {
    return {
      name: this.name,
      damage: this.damage,
      range: this.range,
      fireRate: this.fireRate,
      ammo: this.ammo,
      maxAmmo: this.maxAmmo
    };
  }
}

// Specific weapon types
export class Pistol extends Weapon {
  constructor() {
    super('Pistol', 25, 50, 1000);
    this.maxAmmo = 12;
    this.ammo = this.maxAmmo;
  }
}

export class Rifle extends Weapon {
  constructor() {
    super('Rifle', 40, 100, 800);
    this.maxAmmo = 30;
    this.ammo = this.maxAmmo;
  }
}

export class Shotgun extends Weapon {
  constructor() {
    super('Shotgun', 60, 20, 1500);
    this.maxAmmo = 8;
    this.ammo = this.maxAmmo;
  }
}

// Weapon manager
export class WeaponManager {
  constructor() {
    this.weapons = new Map();
    this.currentWeapon = null;
    this.initWeapons();
  }

  initWeapons() {
    this.weapons.set('pistol', new Pistol());
    this.weapons.set('rifle', new Rifle());
    this.weapons.set('shotgun', new Shotgun());
    this.currentWeapon = this.weapons.get('pistol');
  }

  getWeapon(name) {
    return this.weapons.get(name);
  }

  switchWeapon(name) {
    const weapon = this.weapons.get(name);
    if (weapon) {
      this.currentWeapon = weapon;
      return true;
    }
    return false;
  }

  fire() {
    if (this.currentWeapon && this.currentWeapon.fire()) {
      return true;
    }
    return false;
  }

  reload() {
    if (this.currentWeapon) {
      this.currentWeapon.reload();
      return true;
    }
    return false;
  }

  getStats() {
    return {
      currentWeapon: this.currentWeapon?.getStats(),
      weapons: Array.from(this.weapons.entries()).map(([name, weapon]) => ({
        name,
        stats: weapon.getStats()
      }))
    };
  }
}

// Export default instance
export const weaponManager = new WeaponManager();