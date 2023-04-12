<script setup>
import { ref, onMounted } from "vue";

// define a reactive property to hold the movie data
let movies = ref([]);

function fetchMovies() {
    fetch("/api/v1/movies", {
        method: 'GET'
    })
    .then((response) => response.json())
    .then((data) => {
        // update the movies reactive property with the data
        movies.value = data.movies;
    })
    .catch((error) => {
        console.log(error);
    });
}

onMounted(() => {
    fetchMovies();
});
</script>

<template>
<div class="container mt-4">
    <h1 class="text-center mb-4">All Movies</h1>
    <div class="row">
        <div class="col-md-4 mb-4" v-for="movie in movies" :key="movie.id">
            <div class="card" style="width: 400px;">
                <img :src="movie.poster" class="card-img-top" :alt="movie.title">
                <div class="card-body">
                    <h5 class="card-title">{{ movie.title }}</h5>
                    <p class="card-text">{{ movie.description }}</p>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
  