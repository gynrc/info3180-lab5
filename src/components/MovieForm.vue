<template>
    <div class="container d-flex justify-content-center">
      <form @submit.prevent="saveMovie" method="post" enctype="multipart/form-data" id="movieForm" class="w-50">
        <h1 class="text-center mb-4">Add a Movie</h1>
        <div v-show="showBanner" v-bind:class="[isSuccess ? successMessage : errorMessage]" class="alert">
            {{ flashMessage }}
        </div>
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" id="title" class="form-control"/>
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label">Movie Description</label>
            <textarea name="description" id="description" class="form-control" cols="30" rows="5"></textarea>
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label">Movie Poster</label>
            <input type="file" name="poster" id="poster" class="form-control"/>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    let csrf_token = ref("");
    let successMessage = ref("alert-success");
    let errorMessage = ref("alert-danger");
    let showBanner = ref(false);
    let isSuccess = ref(false);
    let flashMessage = ref("");

    function clearForm() {
        title.value = "";
        description.value = "";
        poster.value = "";
    }

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
            if ("message" in data) {
                console.log(data);
                isSuccess.value = true;
                flashMessage.value = data.message;
                clearForm();
            } else if ("errors" in data) {
                isSuccess.value = false;
                flashMessage.value = data.errors;
            }
            showBanner.value = true;
        })
        .catch(function (error) {
            console.log(error);
            isSuccess.value = false;
            flashMessage.value = "An error occurred.";
            showBanner.value = true;
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