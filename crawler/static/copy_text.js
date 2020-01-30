$(document).ready(function () {
    const button = document.querySelector('#copy');
    const copied_text = document.querySelector('#content');

    function copy_to_clipboard() {
        navigator.clipboard.writeText(copied_text.innerText).then(function () {
            console.log('Copied to clipboard successfully!');
        }).catch(function () {
            console.error('Unable to copy to clipboard');
        });
    }

    button.addEventListener('click', copy_to_clipboard);
});