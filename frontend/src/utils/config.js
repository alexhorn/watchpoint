export let api_base;

// from https://stackoverflow.com/a/35470995
if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    api_base = "http://127.0.0.1:5000/api";
} else {
    api_base = "/api";
}
