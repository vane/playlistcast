import React, { useState } from 'react';
import { resourceLocationAll, resourceLocationAdd, resourceLocationDel } from '../service/resourcelocation';
import resourceLocationStore from '../store/resourceLocationStore';

const ResourceLocationComponent = () => (
  <div>
    <ResourceLocationList />
    <ResourceLocationInput />
  </div>
);

const ResourceLocationList = () => {
  const [locationList, setLocationList] = useState(resourceLocationStore.location);
  const handleLocationChange = () => {
    setLocationList(resourceLocationStore.location);
    console.log('handleLocationChange', resourceLocationStore.location);
  };

  resourceLocationStore.setCallback('location', handleLocationChange);
  resourceLocationAll(resourceLocationStore);

  const locations = [];
  locationList.forEach((el) => {
    locations.push(<ResourceLocationItem key={`location_${el.id}`} data={el} />);
  });
  console.log('render ', locations);
  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Item</th>
            <th> </th>
          </tr>
        </thead>
        <tbody>
          { locations }
        </tbody>
      </table>
    </div>
  );
};

// item
const ResourceLocationItem = (data) => {
  const d = data.data;

  const handleEdit = () => {
    console.log('edit');
  };

  const handleDelete = () => {
    resourceLocationDel(resourceLocationStore, d.name);
  };
  return (
    <tr>
      <td>{d.name}</td>
      <td>{d.location}</td>
      <td>{d.protocol}</td>
      <td>
        <button type="button" onClick={handleEdit}>Edit</button>
        <button type="button" onClick={handleDelete}>Delete</button>
      </td>
    </tr>
  );
};

// input

const ResourceLocationInput = () => {
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');
  const [protocol, setProtocol] = useState('local');

  const handleLocationAdd = () => {
    console.log(`add location ${name} ${location}`);
    resourceLocationAdd(resourceLocationStore, {
      name, location, protocol,
    });
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleLocationChange = (e) => {
    setLocation(e.target.value);
  };

  const handleProtocolChange = (e) => {
    console.log(e);
    setProtocol('local');
  };
  return (
    <div>
      <label htmlFor="name">
        <span>Name : </span>
        <input value={name} onChange={handleNameChange} id="name" type="text" placeholder="name" />
      </label>
      <br />
      <label htmlFor="location">
        <span>Location : </span>
        <input value={location} onChange={handleLocationChange} id="location" type="text" placeholder="name" />
      </label>
      <br />
      <label htmlFor="protocol">
        <span>Protocol : </span>
        <select id="protocol" onChange={handleProtocolChange}>
          <option value="local">Local</option>
        </select>
      </label>
      <button type="button" onClick={handleLocationAdd}>Add</button>
    </div>
  );
};

export default ResourceLocationComponent;
