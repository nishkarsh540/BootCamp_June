<template>
  <div class="product-management">
    <h2>Product Management</h2>

    <!-- Form to Add New Product -->
    <form @submit.prevent="addProduct">
      <h3>Add New Product</h3>
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="newProduct.name" required>
      </div>
      <div>
        <label for="category">Category:</label>
        <select id="category" v-model="newProduct.category_id" required>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>
      <div>
        <label for="expiry_date">Expiry Date:</label>
        <input type="date" id="expiry_date" v-model="newProduct.expiry_date">
      </div>
      <div>
        <label for="manufacture_date">Manufacture Date:</label>
        <input type="date" id="manufacture_date" v-model="newProduct.manufacture_date">
      </div>
      <div>
        <label for="price">Price:</label>
        <input type="number" id="price" v-model="newProduct.price" required>
      </div>
      <div>
        <label for="unit">Unit:</label>
        <input type="text" id="unit" v-model="newProduct.unit" required>
      </div>
      <div>
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity" v-model="newProduct.quantity" required>
      </div>
      <button type="submit">Add Product</button>
    </form>

    <!-- Product List Table -->
    <h3>Existing Products</h3>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Category</th>
          <th>Expiry Date</th>
          <th>Manufacture Date</th>
          <th>Price</th>
          <th>Unit</th>
          <th>Quantity</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>{{ product.name }}</td>
          <td>{{ product.category }}</td>
          <td>{{ product.expiry_date }}</td>
          <td>{{ product.manufacture_date }}</td>
          <td>{{ product.price }}</td>
          <td>{{ product.unit }}</td>
          <td>{{ product.quantity }}</td>
          <td>
            <button @click="editProduct(product)">Edit</button>
            <button @click="deleteProduct(product.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal for Editing Product -->
    <div v-if="editingProduct" class="modal">
      <div class="modal-content">
        <span class="close" @click="cancelEdit">&times;</span>
        <h3>Edit Product</h3>
        <form @submit.prevent="updateProduct">
          <div>
            <label for="edit_name">Name:</label>
            <input type="text" id="edit_name" v-model="editingProduct.name" required>
          </div>
          <div>
            <label for="edit_category">Category:</label>
            <select id="edit_category" v-model="editingProduct.category_id" required>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
          <div>
            <label for="edit_expiry_date">Expiry Date:</label>
            <input type="date" id="edit_expiry_date" v-model="editingProduct.expiry_date">
          </div>
          <div>
            <label for="edit_manufacture_date">Manufacture Date:</label>
            <input type="date" id="edit_manufacture_date" v-model="editingProduct.manufacture_date">
          </div>
          <div>
            <label for="edit_price">Price:</label>
            <input type="number" id="edit_price" v-model="editingProduct.price" required>
          </div>
          <div>
            <label for="edit_unit">Unit:</label>
            <input type="text" id="edit_unit" v-model="editingProduct.unit" required>
          </div>
          <div>
            <label for="edit_quantity">Quantity:</label>
            <input type="number" id="edit_quantity" v-model="editingProduct.quantity" required>
          </div>
          <button type="submit">Update Product</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      categories: [],
      products: [],
      newProduct: {
        name: '',
        category_id: '',
        expiry_date: '',
        manufacture_date: '',
        price: 0,
        unit: '',
        quantity: 0
      },
      editingProduct: null
    };
  },
  created() {
    this.fetchCategories();
    this.fetchProducts();
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
    async fetchProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/products');
        this.products = response.data.products;
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    async addProduct() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/products', this.newProduct);
        this.products.push(response.data.product);
        this.resetNewProductForm();
      } catch (error) {
        console.error('Error adding product:', error);
      }
    },
    resetNewProductForm() {
      this.newProduct = {
        name: '',
        category_id: '',
        expiry_date: '',
        manufacture_date: '',
        price: 0,
        unit: '',
        quantity: 0
      };
    },
    editProduct(product) {
      this.editingProduct = { ...product };
    },
    async updateProduct() {
      try {
        const response = await axios.put(`http://127.0.0.1:5000/products/${this.editingProduct.id}`, this.editingProduct);
        const index = this.products.findIndex(p => p.id === this.editingProduct.id);
        this.products.splice(index, 1, response.data.product);
        this.editingProduct = null;
      } catch (error) {
        console.error('Error updating product:', error);
      }
    },
    cancelEdit() {
      this.editingProduct = null;
    },
    async deleteProduct(productId) {
      try {
        await axios.delete(`http://127.0.0.1:5000/products/${productId}`);
        this.products = this.products.filter(product => product.id !== productId);
      } catch (error) {
        console.error('Error deleting product:', error);
      }
    }
  }
};
</script>

<style scoped>
.product-management {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h2, h3 {
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

form div {
  display: flex;
  justify-content: space-between;
}

form label {
  width: 30%;
}

form input, form select {
  width: 60%;
}

button {
  align-self: center;
  padding: 5px 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table, th, td {
  border: 1px solid #ddd;
}

th, td {
  padding: 8px;
  text-align: left;
}

.actions button {
  margin-right: 5px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}
</style>
