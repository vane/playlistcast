import React from 'react';

const FirstStartComponent = () => (
  <div>
    <label htmlFor="name">
      <span>Name : </span>
      <input id="name" type="text" placeholder="name" />
    </label>
    <br />
    <label htmlFor="location">
      <span>Location : </span>
      <input id="location" type="text" placeholder="name" />
    </label>
    <br />
    <label htmlFor="protocol">
      <span>Protocol : </span>
      <select id="protocol">
        <option>Local</option>
      </select>
    </label>
  </div>
);

export default FirstStartComponent;
