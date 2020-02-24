import React from 'react';
import menuStore from '../store/menuStore';

const MenuComponent = () => {
  const handleLocationClick = () => {
    menuStore.setState({
      index: 'location',
    });
    menuStore.refresh('index');
  };
  return (
    <div>
      <h1>Menu</h1>
      <button type="button" onClick={handleLocationClick}>Location</button>
    </div>
  );
};

export default MenuComponent;
