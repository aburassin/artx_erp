console.log("hello");
document.addEventListener("DOMContentLoaded", function () {
    const lang = document.documentElement.lang; 
    if (lang === "ar") {
        document.body.style.direction = "rtl";
        document.body.style.textAlign = "right";
    } else {
        document.body.style.direction = "ltr";
        document.body.style.textAlign = "left";
    }
});
