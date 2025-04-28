async function send_async_request() {
    const result = await fetch("/cart/", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: 12, title: "finish" })
    });

    console.log("Raw Response:", result);  // Log the raw response object
    const jsonResult = await result.json();
    console.log("API Response:", jsonResult);  // Log the parsed JSON response
}

send_async_request();