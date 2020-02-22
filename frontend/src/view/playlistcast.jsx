import React, { useState } from 'react';
import TimeComponent from './time';
import FirstStartComponent from './firststart';
import firstStartStore from '../store/firstStartStore';
import { firstStartGet } from '../service/firststart';

const PlaylistCast = () => {
  const [firstStart, setFirstStart] = useState(firstStartStore.value);

  const handleFirstStart = () => {
    console.log('change');
    setFirstStart(firstStartStore.value);
  };

  firstStartStore.setCallback('value', handleFirstStart);
  if (firstStart === null) firstStartGet(firstStartStore);
  if (firstStart) {
    return (
      <div>
        <div>
          <FirstStartComponent />
        </div>
        <div>
          <TimeComponent />
        </div>
      </div>
    );
  }
  return (
    <div>
      <h1>Loading...</h1>
    </div>
  );
};

export default PlaylistCast;
