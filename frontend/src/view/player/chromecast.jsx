import React, { useState, useEffect } from 'react';
import { Avatar, Button, Card } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlayCircle, faPauseCircle, faClosedCaptioning } from '@fortawesome/free-regular-svg-icons';
import { faRedo, faUndo, faVolumeUp } from '@fortawesome/free-solid-svg-icons';
import chromecastStore from 'store/chromecastStore';
import { chromecastPause, chromecastPlay, chromecastSeek } from 'service/chromecast';
import TimeDisplay from 'view/player/timeDisplay';
import VolumeComponent from 'view/player/volume';
import CaptionComponent from 'view/player/caption';
import TimeProgress from 'view/player/timeProgress';


const ChromecastDeviceComponent = () => {
  const [chromecastList, setChromecastList] = useState(chromecastStore.chromecast);
  const handleChromecastChange = () => {
    setChromecastList(chromecastStore.chromecast);
  };

  chromecastStore.setCallback('chromecast', handleChromecastChange);
  const device = [];
  chromecastList.forEach((el) => {
    device.push(<ChromecastDevice key={el.uuid} device={el} />);
  });
  return (
    <div>
      <h1>Device</h1>
      <div>
        {device}
      </div>
    </div>
  );
};

const ChromecastDevice = ({ device }) => {
  const mc = device.mediaController;
  const castStatus = device.status;
  const [status, setStatus] = useState(mc.status);
  const [volumeVisible, setVolumeVisible] = useState(false);
  const [captionVisible, setCaptionVisible] = useState(false);

  useEffect(() => {
    const handleStatusChange = () => {
      setStatus(chromecastStore.mediaStatus[device.uuid]);
    };
    chromecastStore.setCallback(device.uuid, handleStatusChange);
    return () => chromecastStore.delCallback(device.uuid);
  });

  const handlePauseClick = () => {
    chromecastPause(device.uuid);
  };

  const handlePlayClick = () => {
    chromecastPlay(device.uuid);
  };

  const handleVolumeChange = () => {
    setCaptionVisible(false);
    setVolumeVisible(!volumeVisible);
  };
  console.log(status.currentTime);
  const hanleSeekForward = () => {
    chromecastSeek(device.uuid, status.currentTime + 30);
  };

  const handleSeekBackward = () => {
    chromecastSeek(device.uuid, status.currentTime - 30);
  };

  const handleCaptionChange = () => {
    setVolumeVisible(false);
    setCaptionVisible(!captionVisible);
  };

  let playPauseButton = null;

  if (status.playerState === 'PLAYING') {
    playPauseButton = (
      <Button
        type="link"
        style={{ marginRight: '10px' }}
        icon={<FontAwesomeIcon icon={faPauseCircle} onClick={handlePauseClick} size="2x" />}
      />
    );
  } else if (status.playerState === 'PAUSED') {
    playPauseButton = (
      <Button
        type="link"
        style={{ marginRight: '10px' }}
        icon={<FontAwesomeIcon icon={faPlayCircle} onClick={handlePlayClick} size="2x" />}
      />
    );
  }

  let name = '';
  let component = null;
  if (status.contentId !== null) {
    name = status.contentId.substring(status.contentId.lastIndexOf('/') + 1);
    let volumeComponent = null;
    if (volumeVisible) {
      volumeComponent = <VolumeComponent uid={device.uuid} volumeLevel={castStatus.volumeLevel} />;
    }
    let captionComponent = null;
    if (captionVisible) {
      captionComponent = (
        <CaptionComponent
          uid={device.uuid}
          trackList={status.trackList}
        />
      );
    }
    component = (
      <div>
        <TimeDisplay
          currentTime={status.currentTime}
          duration={status.duration}
          playerState={status.playerState}
        />
        <TimeProgress
          uid={device.uuid}
          currentTime={status.currentTime}
          duration={status.duration}
          playerState={status.playerState}
        />
        <div>
          <Button
            type="link"
            style={{ marginRight: '10px' }}
            icon={<FontAwesomeIcon icon={faUndo} onClick={handleSeekBackward} size="2x" />}
          />
          <Button
            type="link"
            style={{ marginRight: '10px' }}
            icon={<FontAwesomeIcon icon={faVolumeUp} onClick={handleVolumeChange} size="2x" />}
          />
          {playPauseButton}
          <Button
            type="link"
            style={{ marginRight: '10px' }}
            icon={<FontAwesomeIcon icon={faRedo} onClick={hanleSeekForward} size="2x" />}
          />
          <Button
            type="link"
            style={{ marginRight: '10px' }}
            icon={<FontAwesomeIcon icon={faClosedCaptioning} onClick={handleCaptionChange} size="2x" />}
          />
        </div>
        {volumeComponent}
        {captionComponent}
      </div>
    );
  }
  return (
    <Card title={
      (
        <span>
          <Avatar src={castStatus.iconUrl} />
          <span style={{ marginLeft: '10px' }}>{device.name}</span>
        </span>
      )
    }
    >
      <div>
        <p>{name}</p>
        {component}
      </div>
    </Card>
  );
};

export default ChromecastDeviceComponent;
