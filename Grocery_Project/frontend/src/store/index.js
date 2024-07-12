// store/index.js
import { createStore } from 'vuex';
import router from '../router';
import {jwtDecode} from 'jwt-decode';

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || null
  },
  getters: {
    isAuthenticated: state => !!state.token,
    userRole: state => {
      if (state.token) {
        const decoded = jwtDecode(state.token);
        return decoded.sub;
      }
      return null;
    }
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem('token', token);
        const decoded  = jwtDecode(token)
        state.user = {role:decoded.role};
        console.log(decoded.sub);
      } else {
        localStorage.removeItem('token');
        state.user= null;
        localStorage.removeItem('user')
      }
    },
    setUser(state, user) {
      state.user = user;
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
      } else {
        localStorage.removeItem('user');
      }
    },
    logout(state) {
      state.token = '';
      state.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');

    }
  },
  actions: {
    login({ commit }, { token }) {
      commit('setToken', token);
    },
    logout({ commit }) {
      commit('logout');
      router.push('/login');
    }
  }
});
