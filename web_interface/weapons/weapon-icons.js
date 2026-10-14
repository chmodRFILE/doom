// Weapon icon system

// Icon component for weapons
export const WeaponIcon = ({ weaponName, size = 24, className = '' }) => {
  const icons = {
    pistol: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
      </svg>
    ),
    rifle: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
        <line x1="12" y1="8" x2="12" y2="16" />
      </svg>
    ),
    shotgun: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
        <circle cx="12" cy="12" r="3" />
      </svg>
    )
  };

  return icons[weaponName] || null;
};

// Weapon icon list component
export const WeaponIconList = ({ weapons, onWeaponSelect, selectedWeapon }) => {
  return (
    <div className="weapon-icon-list">
      {weapons.map((weapon) => (
        <button
          key={weapon.name}
          className={`weapon-icon ${selectedWeapon === weapon.name ? 'selected' : ''}`}
          onClick={() => onWeaponSelect(weapon.name)}
        >
          <WeaponIcon weaponName={weapon.name} size={24} />
          <span>{weapon.name}</span>
        </button>
      ))}
    </div>
  );
};