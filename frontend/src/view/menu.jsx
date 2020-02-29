import React from 'react';
import menuStore from '../store/menuStore';
import chromecastDeviceAll from '../service/device';
import deviceStore from '../store/deviceStore';
import { resourceLocationAll } from '../service/resourceLocation';
import resourceLocationStore from '../store/resourceLocationStore';

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
    resourceLocationAll(resourceLocationStore);
  };

  const handleDeviceClick = () => {
    menuStore.setState({
      index: 'chromecast',
    });
    menuStore.refresh('index');
    chromecastDeviceAll(deviceStore);
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
