$(document).ready(function () {
    $("#register")
        .bootstrapValidator({
            fields: {
                username: {
                    validators: {
                        notEmpty: {
                            message:
                                "Le nom d'ulisateur est réquis et ne peut être vide",
                        },
                    },
                },
                email: {
                    validators: {
                        notEmpty: {
                            message:
                                "L'adresse courriel est réquise et ne peut être vide",
                        },
                        emailAddress: {
                            message: "L'adresse courriel n'est pas valide"
                        }
                    },
                },
                password: {
                    validators: {
                        notEmpty: {
                            message:
                                "Le mot de passe est réquis et ne peut être vide",
                        },
                        different: {
                            field: 'username',
                            message: "Le mot de passe doit être différent du nom d'utilisateur"
                        },
                        stringLength: {
                            min: 6,
                            message: 'Le mot de passe doit contenir au 6 caractères'
                        }
                    },
                },
            },
        })
        .on("success.form.bv", function (e) {
            // Prevent form submission
            e.preventDefault();

            var data = {
                username: $("#username").val(),
                email: $("#email").val(),
                etablissements: $("#etablissement_autocomplete").val().split(','),
                password: $("#password").val()
            };
            register(data, $("#edit-from").val());
        });
});

function register(data) {
    fetch(`${window.location.origin}/users`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    }).then((response) => {
        //return response.json();
        var Toast = Swal.mixin({
            toast: true,
            position: "top-end",
            showConfirmButton: false,
            timer: 2000,
            timerProgressBar: true,
            onOpen: (toast) => {
                toast.addEventListener("mouseenter", Swal.stopTimer);
                toast.addEventListener("mouseleave", Swal.resumeTimer);
            },
            onClose: () => {
                window.location.href = `${window.location.origin}/account/login`
            }
        });
        if (!response.ok) {
            Toast.fire({
                icon: "error",
                title: "Une erreur s'est produite",
            });
        } else
            Toast.fire({
                icon: "success",
                title: "Inscription éffectuée avec succès",
            });
    })
        .catch((data) => {
            console.log(data);
        });
}