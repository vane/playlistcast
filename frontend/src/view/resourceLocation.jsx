import React, { useState } from 'react';
import { resourceLocationAdd, resourceLocationDel, resourceLocationChange } from 'service/resourceLocation';
import resourceLocationStore from 'store/resourceLocationStore';

const ResourceLocationComponent = () => (
  <div>
    <ResourceLocationTable />
    <ResourceLocationInput />
  </div>
);

const ResourceLocationTable = () => {
  const [locationList, setLocationList] = useState(resourceLocationStore.location);
  const handleLocationChange = () => {
    setLocationList(resourceLocationStore.location);
    console.log('handleLocationChange', resourceLocationStore.location);
  };

  resourceLocationStore.setCallback('location', handleLocationChange);

  const locations = [];
  locationList.forEach((el) => {
    locations.push(<ResourceLocationRow key={`location_${el.id}`} data={el} />);
  });
  console.log('render ', locations);
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Location</th>
          <th>Protocol</th>
          <th> </th>
        </tr>
      </thead>
      <tbody>
        { locations }
      </tbody>
    </table>
  );
};

// item
const ResourceLocationRow = ({ data }) => {
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(data.name);
  const [location, setLocation] = useState(data.location);
  const [protocol, setProtocol] = useState(data.protocol);

  const handleEdit = () => {
    console.log('edit');
    setEditing(true);
  };

  const handleDelete = () => {
    resourceLocationDel(resourceLocationStore, data.id);
  };

  const handleSave = () => {
    resourceLocationChange(resourceLocationStore, { name, location, protocol }, data.id);
    setEditing(false);
  };

  const handleCancel = () => {
    setName(data.name);
    setLocation(data.location);
    setProtocol(data.protocol);
    setEditing(false);
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleLocationChange = (e) => {
    setLocation(e.target.value);
  };

  const handleProtocolChange = (e) => {
    setProtocol(e.target.value);
  };

  if (editing) {
    return (
      <tr>
        <td><input type="text" value={name} onChange={handleNameChange} /></td>
        <td><input type="text" value={location} onChange={handleLocationChange} /></td>
        <td><input type="text" value={protocol} onChange={handleProtocolChange} /></td>
        <td>
          <button type="button" onClick={handleSave}>Save</button>
          <button type="button" onClick={handleCancel}>Cancel</button>
        </td>
      </tr>
    );
  }
  return (
    <tr>
      <td><a href={`/resource/${name}`}>{name}</a></td>
      <td>{location}</td>
      <td>{protocol}</td>
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
