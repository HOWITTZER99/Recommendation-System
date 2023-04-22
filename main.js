const app = new Vue({
    el: '#app',
    data: {
      movie: '',
      recommendations: []
    },
    methods: {
      async getRecommendations() {
        try {
          const response = await axios.post('/recommend', {movie: this.movie});
          this.recommendations = response.data;
        } catch (error) {
          console.error(error);
        }
      }
    }
  });
  