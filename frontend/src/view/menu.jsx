import React from 'react';
import menuStore from '../store/menuStore';

const container = {
  display: 'flex',
  flexDirection: 'column',
};

const MenuComponent = () => {
  const handleLocationClick = () => {
    menuStore.setState({
      index: 'location',
    });
    menuStore.refresh('index');
  };

  const handleDeviceClick = () => {
    menuStore.setState({
      index: 'device',
    });
    menuStore.refresh('index');
  };
  return (
    <div>
      <h1>Menu</h1>
      <div style={container}>
        <button type="button" onClick={handleLocationClick}>Location</button>
        <button type="button" onClick={handleDeviceClick}>Device</button>
      </div>
    </div>
  );
};

export default MenuComponent;
