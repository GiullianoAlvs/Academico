function buttonClickAnimation(button) {
    button.classList.add("clicked");
    setTimeout(function () {
        button.classList.remove("clicked");
    }, 200);
}