<template>
  <div class="admin-dashboard">
    <h2>Admin Dashboard - Store Managers</h2>
    <ul class="store-manager-list">
      <li v-for="manager in storeManagers" :key="manager.id" class="store-manager-item">
        <p><strong>Username:</strong> {{ manager.username }}</p>
        <p><strong>Email:</strong> {{ manager.email }}</p>
        <p><strong>Status:</strong> {{ manager.is_active ? 'Active' : 'Inactive' }}</p>
        <div class="actions">
          <button v-if="!manager.is_active" @click="handleAction(manager.id, 'approve')">Approve</button>
          <button @click="handleAction(manager.id, 'delete')">Delete</button>
          <button v-if="manager.is_active" @click="handleAction(manager.id, 'flag')">Flag</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      storeManagers: [],
    };
  },
  created() {
    this.fetchStoreManagers();
  },
  methods: {
    async fetchStoreManagers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/store-managers');
        this.storeManagers = response.data.store_managers;
      } catch (error) {
        console.error('Error fetching store managers:', error);
      }
    },
    async handleAction(userId, action) {
      try {
        const response = await axios.post(`http://127.0.0.1:5000/store-managers/${userId}/${action}`);
        alert(response.data.message);
        this.fetchStoreManagers(); // Refresh the list after action
      } catch (error) {
        console.error(`Error performing ${action} action:`, error);
      }
    },
  },
};
</script>

<style scoped>
.admin-dashboard {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: left;
}

h2 {
  text-align: center;
  font-size: 2em;
  margin-bottom: 20px;
}

.store-manager-list {
  list-style-type: none;
  padding: 0;
}

.store-manager-item {
  padding: 10px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
  border-radius: 4px;
}

.store-manager-item p {
  margin: 5px 0;
}

.actions button {
  margin-right: 10px;
}
</style>
