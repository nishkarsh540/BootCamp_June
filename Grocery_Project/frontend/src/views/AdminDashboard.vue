<template>
  <h2>hello</h2>
  <button @click="exportCSV">
    Download Report
  </button>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    exportCSV() {
      const accessToken = localStorage.getItem('token');
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios.post('http://127.0.0.1:5000/exportcsv/1', {}, { headers, responseType: 'blob' })
        .then(response => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const downloadLink = document.createElement('a');
          downloadLink.href = url;
          downloadLink.setAttribute('download', 'product_report.csv');

          document.body.appendChild(downloadLink);
          downloadLink.click();
          document.body.removeChild(downloadLink);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>
