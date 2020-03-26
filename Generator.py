import os
import shutil
from tkinter import messagebox
import sys


class Generator:
    def __init__(self, src, type_name, file_name, api_f_name, action_name):
        self.IsCall = True
        self.src = self.is_empty(src, 'path')
        self.typeName = self.is_empty(type_name, 'type name')
        self.fileName = self.is_empty(file_name, 'File name')
        self.api_f_name = self.is_empty(api_f_name, 'api method name')
        self.action_name = self.is_empty(action_name, 'action name')
        self.duckSrc = src + 'state/ducks/' + file_name + "/"
        self.viewsSrc = src + 'views/' + file_name + "/"

        self.create_file(self.duckSrc)
        self.create_file(self.viewsSrc)
        print(self.IsCall)
        if self.IsCall:
            self.call()

    def is_empty(self, field, file_name):
        if not field and self.IsCall:
            self.IsCall = False
            messagebox.showerror(
                'Failed', '%s is empty please check it' % file_name)
        return field

    def call(self):
        self.create_reducer()
        self.create_operations()
        self.create_type()
        self.create_action()
        self.create_views()
        self.create_package_json()
        self.create_view_style()
        self.create_container()
        self.create_story()
        self.create_test()
        self.create_index()
        self.add_store()

    def create_type(self):
        text = '''const %(type)s = '%(type)s/%(name)s';
const %(type)s_FAILED = '%(type)s_FAILED/%(name)s';
const %(type)s_SUCCESS = '%(type)s_SUCCESS/%(name)s';
export default{  %(type)s, %(type)s_SUCCESS, %(type)s_FAILED }
        ''' % {"type": self.typeName, "name": self.fileName}
        f = open(self.duckSrc + 'types.js', 'a')
        f.write(text)
        f.close()

    def create_action(self):
        action = """
        import  type from './types';
        export const %(action_name)s = (payload) => ({
            type: type.%(type)s,
            payload
        });""" % {"type": self.typeName, "action_name": self.action_name, 'api_f_name': self.api_f_name}
        f = open(self.duckSrc + 'actions.js', 'a')
        f.write(action)
        f.close()

    def create_index(self):
        text = '''import reducer from './reducers';
export { default as %(name)sOperations } from './operations';
export { default as %(name)sTypes } from './types';

export default reducer;''' % {"type": self.typeName, "name": self.fileName, 'api_f_name': self.api_f_name}
        f = open(self.duckSrc + 'index.js', 'a')
        f.write(text)
        f.close()

    def add_store(self):
        text = '''export { default as %(name)s } from './%(name)s';''' % {
            "name": self.fileName}
        f = open(self.src + 'state/ducks/index.js', 'a')
        f.write(text)
        f.close()

    def create_reducer(self):
        reducer = """import type from './types';
const INITIAL_STATE = {
    loader: false,
    error: '',
    data: [],
};
const %(name)s = (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case type.%(type)s:
          return {
            ...state,
            loader: true,
          };
        case type.%(type)s_SUCCESS:
          return {
            ...state,
            loader: false,
            data: action.data,
          };
        case type.%(type)s_FAILED:
          return {
            ...state,
            loader: false,
            error: action.error,
          };
        
        default:
          return state;
    }
};
export default %(name)s;""" % {"type": self.typeName, "name": self.fileName}
        f = open(self.duckSrc + 'reducers.js', 'a')
        f.write(reducer)
        f.close()
        print('Reducer created')

    def create_operations(self):
        operations = """
import { put, takeLatest } from 'redux-saga/effects';
import api from '@duck_utils/api';
import type from './types';
export function* %(action_name)s(action) {
  try {
    const response = yield api.%(api_f_name)s(action.payload);
    if (response.hasOwnProperty('error')) {
      yield put({
        type: type.%(type)s_FAILED,
        error: response.error,
      });
    } else {
      yield put({
        type: type.%(type)s_SUCCESS,
        data: response.data,
      });
    }
  } catch (error) {
    yield put({
      type: type.%(type)s_FAILED,
      error,
    });
  }
}

export default function* watch_%(action_name)s() {
  yield takeLatest(type.%(type)s, %(action_name)s);
}  """ % {"type": self.typeName, "name": self.fileName, 'api_f_name': self.api_f_name, 'action_name': self.action_name}
        f = open(self.duckSrc + 'operations.js', 'a')
        f.write(operations)
        f.close()
        print('operations created')

    def create_file(self, folder):
        if os.path.exists(folder) and self.IsCall:
            self.IsCall = False
            messagebox.showerror(
                'Failed', 'folder is exist in this location ({0})  please check it'.format(folder))

        elif self.IsCall:
            os.makedirs(folder)

    def create_package_json(self):
        text = """{
  "name": "@%s"
}
""" % self.fileName
        f = open(self.duckSrc + 'package.json', 'a')
        f.write(text)
        print('package.json created')

    def create_views(self):
        text = ''' 
import React, { PureComponent } from 'react';
import { View, Text } from 'react-native'; 
import { Button } from 'components'; 
import { styles} from './style';  

class %(name)s extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {};
  } 
  render() {
    return (
        <View style={styles.container}> 
            <Text>
                %(name)s 
            </Text>  
        </View>
    );
  }
} 
export default %(name)s  
        ''' % {"type": self.typeName, "name": self.fileName.capitalize(), 'api_f_name': self.api_f_name}
        f = open(self.viewsSrc + 'index.js', 'a')
        f.write(text)
        f.close()
        print('index.js created')

    def create_view_style(self):
        style = '''
import { StyleSheet } from 'react-native';
import { colors } from 'config'; 
export const styles = StyleSheet.create({
  container: { 
    flex: 1,
    justifyContent:'center'
  },
});'''
        f = open(self.viewsSrc + 'style.js', 'a')
        f.write(style)
        f.close()
        print('style.js created')

    def create_container(self):
        style = '''
import { connect } from 'react-redux';
import  %(name)s from './index'; 
import { %(action_name)s } from '@%(file_name)s/actions' ; 
const mapStateToProps = state => {
  return {
    data: state.%(file_name)s.data,
    error:state.%(file_name)s.error,
    loading:state.%(file_name)s.loading
  };
};
const mapStateToDispatch = dispatch => {
  return {
     %(action_name)s: (payload) => dispatch( %(action_name)s(payload)),
};
};

export default connect(mapStateToProps, mapStateToDispatch)( %(name)s);
        ''' % {"type": self.typeName, "name": self.fileName.capitalize(), "file_name": self.fileName,
               'api_f_name': self.api_f_name,
               'action_name': self.action_name}

        f = open(self.viewsSrc + 'container.js', 'a')
        f.write(style)
        f.close()
        print('container.js created')

    def create_story(self):
        story = '''
import React from 'react';
import { storiesOf } from '@storybook/react-native';
import { action } from '@storybook/addon-actions';
import %(name)s from './'; 
import { BufferView } from 'components/decorator';

storiesOf('%(name)s', module)
  .addDecorator(BufferView)
  .add('default', () => {
    return <%(name)s />;
  }) 
''' % {"type": self.typeName, "name": self.fileName.capitalize(), "file_name": self.fileName,
            'api_f_name': self.api_f_name,
            'action_name': self.action_name}

        f = open(self.viewsSrc + self.fileName + '.stories.js', 'a')
        f.write(story)
        f.close()
        print('stories.js created')

    def create_test(self):
        test = '''
import { shallow } from 'enzyme';
import React from 'react';
import toJson from 'enzyme-to-json';
import %(name)s  from './';
describe('%(name)s', () => {
    it('should render without issues', () => {
        const component = shallow(
            <%(name)s />,
        );
        expect(component.length).toBe(1);
        expect(toJson(component)).toMatchSnapshot();
    });
});
        ''' % {"name": self.fileName.capitalize(), }

        f = open(self.viewsSrc + self.fileName + '.test.js', 'a')
        f.write(test)
        f.close()
        print('test.js created')
