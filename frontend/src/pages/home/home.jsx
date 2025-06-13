import React from "react";

// Import hooks
import useCallApi from "../../hooks/callApi.jsx";

const Home = () => {
    // Call the API using the custom hook
    const { data, error, isLoading } = useCallApi("/");

    if (isLoading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error: {error}</div>;
    }
    if (!data) {
        return <div>No data available</div>;
    }

  return (
    <div className="home">
      <h1>Welcome to the Home Page</h1>
      <p>This is the home page of our application.</p>
        <h2>Data from API:</h2>
        <pre>{JSON.stringify(data, null, 2)}</pre>
        <p>Feel free to explore the application!</p>
    </div>
  );
}

export default Home;