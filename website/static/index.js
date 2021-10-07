// javascript function to delete note
function deleteNote(noteId) {
    // to send a request in vannila js (plain js without libraries or frameworks) we use fetch
    // this is a basic way to send a request using js to the backend 
    fetch('/delete-note', { // send a POST request to the backend
        method: 'POST',
        body: JSON.stringify({noteId: noteId}) // the body of the POST request will contain a string represents a json (note id)
    }).then((_res) => { // response
        // refresh the homepage (page we are currently on) after node is deleted (after response)
        window.location.href = "/"; // this is a GET request
    });
}