<template>
  <div class="category-management">
    <h2>Category Management</h2>

    <!-- Form to add a new category -->
    <form @submit.prevent="addCategory">
      <input type="text" v-model="newCategoryName" placeholder="Enter category name" required>
      <button type="submit">Add Category</button>
    </form>

    <!-- Display existing categories in a table -->
    <table v-if="categories.length > 0">
      <thead>
        <tr>  
          <th>ID</th>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="category in categories" :key="category.id">
          <td>{{ category.id }}</td>
          <td>
            <input type="text" v-model="category.name" :disabled="category.id === editingCategoryId">
          </td>
          <td>
            <button v-if="category.id !== editingCategoryId" @click="startEditing(category)">Edit</button>
            <button v-else @click="saveCategory(category)">Save</button>
            <button @click="deleteCategory(category)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Message for no categories -->
    <div v-else>
      <p>No categories found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      categories: [],
      newCategoryName: '',
      editingCategoryId: null
    };
  },
  mounted() {
    this.loadCategories();
  },
  methods: {
    async loadCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/category');
        this.categories = response.data;
      } catch (error) {
        console.error('Error loading categories:', error);
      }
    },
    async addCategory() {
      try {
        const response = await axios.post(' http://127.0.0.1:5000/api/category', {
          name: this.newCategoryName
        });
        console.log('Category added:', response.data);
        this.newCategoryName = ''; // Clear input field
        this.loadCategories();
      } catch (error) {
        console.error('Error adding category:', error);
      }
    },
    async deleteCategory(category) {
      try {
        const response = await axios.delete(' http://127.0.0.1:5000/api/category', {
          data: { id: category.id }
        });
        console.log('Category deleted:', response.data);
        this.loadCategories();
      } catch (error) {
        console.error('Error deleting category:', error);
      }
    },
    async saveCategory(category) {
      try {
        const response = await axios.put(' http://127.0.0.1:5000/api/category', {
          id: category.id,
          name: category.name
        });
        console.log('Category updated:', response.data);
        this.editingCategoryId = null; // Exit edit mode
        this.loadCategories();
      } catch (error) {
        console.error('Error updating category:', error);
      }
    },
    startEditing(category) {
      this.editingCategoryId = category.id;
    }
  }
};
</script>

<style scoped>
.category-management {
  max-width: 800px;
  margin: 0 auto;
}

.category-management form {
  margin-bottom: 1rem;
}

.category-management table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.category-management th, .category-management td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.category-management th {
  background-color: #f2f2f2;
}

.category-management input[type="text"] {
  width: calc(100% - 20px); /* Adjust input width to fit within table cell */
  margin: 0;
}

.category-management button {
  cursor: pointer;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  margin: 2px;
}

.category-management button:hover {
  background-color: #0056b3;
}
</style>
