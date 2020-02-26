import React, { useState } from 'react';
import TimeComponent from './time';
import FirstStartComponent from './firststart';
import firstStartStore from '../store/firstStartStore';
import menuStore from '../store/menuStore';
import { firstStartGet } from '../service/firststart';
import MenuComponent from './menu';
import ResourceLocationComponent from './resourcelocation';


/* Styles */
const container = {
  display: 'flex',
};

const content = {
  paddingLeft: '20px',
};

/* Components */

const PlaylistCast = () => {
  const [firstStart, setFirstStart] = useState(firstStartStore.value);
  const [menuIndex, setMenuIndex] = useState(menuStore.index);

  const handleFirstStart = () => {
    console.log('change');
    setFirstStart(firstStartStore.value);
  };

  const handleMenuIndexChange = () => {
    console.log('handleMenuIndexChange');
    setMenuIndex(menuStore.index);
  };

  firstStartStore.setCallback('value', handleFirstStart);
  menuStore.setCallback('index', handleMenuIndexChange);
  let component = null;
  if (firstStart === null) firstStartGet(firstStartStore);
  if (menuIndex === 'location') {
    component = <ResourceLocationComponent />;
  }
  let startComponent = null;
  if (firstStart) {
    startComponent = <FirstStartComponent />;
  }
  return (
    <div style={container}>
      <div>
        {startComponent}
      </div>
      <div>
        <MenuComponent />
      </div>
      <div style={content}>
        {component}
      </div>
      <div>
        <TimeComponent />
      </div>
    </div>
  );
};

export default PlaylistCast;
