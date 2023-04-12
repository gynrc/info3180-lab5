<template>
    <div class="container d-flex justify-content-center">
      <form @submit.prevent="saveMovie" id="movieForm" class="w-50">
        <h1 class="text-center mb-4">Add a Movie</h1>
        <div v-if="showBanner && successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
        </div>
        <div v-if="showBanner && successMessage" class="alert alert-danger" role="alert">
            <ul>
                <li v-for="error in errorMessage">{{ error }}</li>
            </ul>
        </div>
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" class="form-control"/>
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label">Movie Description</label>
            <input type="text" name="description" class="form-control"/>
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label">Movie Poster</label>
            <input type="file" name="poster" class="form-control"/>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
let csrf_token = ref("");
let successMessage = ref("");
let errorMessage = ref([]);
let showBanner = ref(false);

function saveMovie() {
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);

    fetch("http://localhost:8080/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        successMessage.value = data.message;
        showBanner.value = true;
    })
    .catch(function (error) {
        console.log(error);
        showBanner.value = true;
    });

}

onMounted(() => {
    getCsrfToken();
});

function getCsrfToken() {
    fetch('http://localhost:8080/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
}
</script>