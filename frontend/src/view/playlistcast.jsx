import React, { useState } from 'react';
import { Layout } from 'antd';
import menuStore from '../store/menuStore';
import TimeComponent from './time';
import MenuComponent from './menu';
import ResourceLocationComponent from './resourceLocation';
import ChromecastDeviceComponent from './player/chromecast';

const {
  Content,
  Footer,
  Sider,
} = Layout;

/* Styles */
const slider = {
  overflow: 'auto',
  height: '100vh',
  position: 'fixed',
  left: 0,
};

const contentStyle = {
  margin: '24px 16px 0',
  overflow: 'initial',
};

const PlaylistCast = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [menuIndex, setMenuIndex] = useState(menuStore.index);

  const handleCollapse = (c) => {
    setCollapsed(c);
  };

  const handleMenuIndexChange = () => {
    setMenuIndex(menuStore.index);
  };

  menuStore.setCallback('index', handleMenuIndexChange);

  let component = null;
  if (menuIndex === 'location') {
    component = <ResourceLocationComponent />;
  } else if (menuIndex === 'chromecast') {
    component = <ChromecastDeviceComponent />;
  }

  return (
    <Layout>
      <Sider collapsible collapsed={collapsed} onCollapse={handleCollapse} style={slider}>
        <MenuComponent />
      </Sider>
      <Layout className="site-layout" style={{ marginLeft: collapsed ? 80 : 200 }}>
        <Content style={contentStyle}>
          <div className="site-layout-background">
            <TimeComponent />
            {component}
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>vane.pl © 2020</Footer>
      </Layout>
    </Layout>
  );
};

export default PlaylistCast;
