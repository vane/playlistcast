
export class Store {
  constructor(data) {
    this.callbacks = {};
    this.initialized = false;
    Object.keys(data).forEach((key) => {
      this[key] = data[key];
    });
  }

  setState(data) {
    this.initialized = true;
    // console.log(data);
    Object.keys(data).forEach((key) => {
      this[key] = data[key];
    });
    return this;
  }

  setCallback(name, callback) {
    this.callbacks[name] = callback;
  }

  delCallback(name) {
    delete this.callbacks[name];
  }

  refresh(name) {
    const isName = !!name;
    if (isName) {
      // console.log(`state.Store refresh ${name}`);
      if (this.callbacks[name]) this.callbacks[name]();
    } else {
      Object.keys(this.callbacks).forEach((key) => {
        console.log(`state.Store refresh ${key}`);
        this.callbacks[key]();
      });
    }
  }
}

export const EditableObject = {
  get(data) {
    return { edit: {}, isEditing: false, data };
  },
  edit(data) {
    return { edit: {}, isEditing: true, data: data.data };
  },
  save(data) {
    const output = { ...data.data };
    Object.keys(data.edit).forEach((key) => {
      if (key.indexOf('.') > 0) {
        console.warn('TODO verify');
        // split keys
        const keys = key.split('.');
        let temp = data.data;
        let tempKey = keys[0];
        // get nested object
        let i = 0;
        for (i; i < keys.length - 1; i += 1) {
          tempKey = keys[i];
          if (tempKey in temp) {
            temp = temp[tempKey];
          }
        }
        // get last key and update object
        tempKey = keys[i + 1];
        if (tempKey in temp) {
          temp[tempKey] = data.edit[key];
        }
      } else if (key in data.data) {
        // TODO verify if working good
        output[key] = data.edit[key];
      }
    });
    return { edit: {}, isEditing: false, data: output };
  },
  update(data, second) {
    // TODO verify if working good
    const output = { ...data };
    output.data = { ...second };
  },
  cancel(data) {
    return { edit: {}, isEditing: false, data: data.data };
  },
};
