<template>
  <div class="category-container">
    <h2>Categories</h2>
    <input type="text" v-model="searchQuery" placeholder="Search categories" class="search-bar" />
    <ul class="category-list">
      <li v-for="category in filteredCategories" :key="category.id" class="category-item">
        {{ category.name }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: '',
      categories: [],
    };
  },
  computed: {
    filteredCategories() {
      return this.categories.filter(category =>
        category.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/category');
        this.categories = response.data;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
  },
};
</script>

<style scoped>
.category-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

h2 {
  font-size: 2em;
  margin-bottom: 20px;
}

.search-bar {
  width: 100%;
  padding: 10px;
  font-size: 1em;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.category-list {
  list-style-type: none;
  padding: 0;
}

.category-item {
  padding: 10px;
  font-size: 1.2em;
  border-bottom: 1px solid #eee;
}

.category-item:last-child {
  border-bottom: none;
}

.category-item:hover {
  background-color: #f9f9f9;
}
</style>
