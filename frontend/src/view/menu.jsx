import React, { useState } from 'react';
import { Menu } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChromecast } from '@fortawesome/free-brands-svg-icons';
import { faFolderOpen } from '@fortawesome/free-regular-svg-icons';
import menuStore from '../store/menuStore';
import { chromecastDeviceAll } from '../service/chromecast';
import chromecastStore from '../store/chromecastStore';
import { resourceLocationAll } from '../service/resourceLocation';
import resourceLocationStore from '../store/resourceLocationStore';

const menuItem = {
  padding: '0 0 0 20px',
  fontSize: '1.4em',
};

const MenuComponent = () => {
  const [menuIndex, setMenuIndex] = useState(menuStore.index);

  const handleSelect = ({ key }) => {
    if (key === 'chromecast') {
      chromecastDeviceAll(chromecastStore).then(() => {
        setMenuIndex(key);
        menuStore.setState({ index: key });
        menuStore.refresh('index');
      });
    } else if (key === 'location') {
      resourceLocationAll(resourceLocationStore).then(() => {
        setMenuIndex(key);
        menuStore.setState({ index: key });
        menuStore.refresh('index');
      });
    }
  };

  return (
    <Menu
      theme="dark"
      mode="inline"
      defaultSelectedKeys={[menuIndex]}
      inlineIndent={0}
      onSelect={handleSelect}
    >
      <Menu.Item key="location">
        <FontAwesomeIcon icon={faFolderOpen} size="2x" />
        <span style={menuItem}>Location</span>
      </Menu.Item>
      <Menu.Item key="chromecast">
        <FontAwesomeIcon icon={faChromecast} size="2x" />
        <span style={menuItem}>Chromecast</span>
      </Menu.Item>
    </Menu>
  );
};

export default MenuComponent;
