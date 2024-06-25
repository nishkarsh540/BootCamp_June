import { createStore } from 'vuex';
import axios from 'axios';
import router from '../router';
import { jwtDecode } from 'jwt-decode';
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
        localStorage.setItem('access_token', token);
        const decoded = jwtDecode(token);
        state.user = { role: decoded.role };
      } else {
        localStorage.removeItem('access_token');
        state.user = null;
        localStorage.removeItem('user');
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
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
  },
  actions: {
    login({ commit }, { token }) {
      commit('setToken', token);
    },
    logout({ commit, state }) {
      if (!state.token) {
        console.error('No token found in state. Logout action aborted.');
        return;
      }

      axios.post(' http://127.0.0.1:5000/logout', null, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.token}`
        }
      })
      .then(response => {
        if (response.status === 200) {
          commit('logout');
          router.push('/login');
        } else {
          console.error('Logout failed:', response.statusText);
        }
      })
      .catch(error => {
        console.error('Logout error:', error);
      });
    }
  }
});
