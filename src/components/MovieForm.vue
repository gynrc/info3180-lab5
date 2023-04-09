<template>
    <form @submit.prevent="saveMovie" id="movieForm">
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" class="form-control"/>
        </div>
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Description</label>
            <input type="text" name="decription" class="form-control"/>
        </div>
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Poster</label>
            <input type="text" name="poster" class="form-control"/>
        </div>
        <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
        </div>
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
            <ul>
                <li v-for="error in errorMessage">{{ error }}</li>
            </ul>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
let csrf_token = ref("");
let successMessage = ref("");
let errorMessage = ref([]);

function saveMovie() {
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);

    fetch("/api/v1/movies", {
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
        // display a success message
        successMessage.value = data.message;
    })
    .catch(function (error) {
        errorMessage.value = Object.values(error.response.data.errors);
    });
}

onMounted(() => {
    getCsrfToken();
});


function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
}
</script>