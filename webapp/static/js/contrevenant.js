$("#edit_contrevenant").on("show.bs.modal", function (e) {
    var contrevenant = e.relatedTarget.dataset;
    console.log(contrevenant);
    $("#contrevenant-id").val(contrevenant.id);
    $("#contrevenant-proprietaire").val(contrevenant.proprietaire);
    $("#contrevenant-etablissement").val(contrevenant.etablissement);
    $("#contrevenant-adresse").val(contrevenant.adresse);
    $("#contrevenant-ville").val(contrevenant.ville);
    $("#contrevenant-categorie").val(contrevenant.categorie);
    $("#edit-from").val(contrevenant.from);
});

$("#btnUpdateContrevenant").click(function (e) {
    $(".contrevenantEditionForm").submit();
});

function delete_contrevenant(id) {
    Swal.fire({
        title: "Suppression de contrevenant!",
        text: "Voulez-vous vraiment supprimer ce contrevenant ?",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: "Non",
        confirmButtonText: "Oui",
        preConfirm: function () {
            return fetch(`${window.location.origin}/contrevenants/${id}`, {
                method: "DELETE",
            })
                .then((response) => {
                    console.log(response);
                    if (!response.ok) {
                        throw new Error(response.statusText);
                    }
                    Swal.fire({
                        title: "Suppression de contravention!",
                        text: "La contravention a été supprimée avec succès",
                        icon: "success",
                        preConfirm: function () {
                            location.reload();
                        },
                    });
                })
                .catch((error) => {
                    Swal.showValidationMessage(`Request failed: ${error}`);
                });
        },
    });
}

function update_contrevenant(data, from) {
    console.log(data);
    fetch(`${window.location.origin}/contrevenants/${data.id}`, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
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
                    location.reload();
                },
            });
            if (!response.ok) {
                Toast.fire({
                    icon: "error",
                    title: "Une erreur s'est produite",
                });
            } else
                Toast.fire({
                    icon: "success",
                    title: "La mise à jour éffectué avec succès",
                });
        })
        .catch((data) => {
            console.log(data);
        });
}


$(document).ready(function () {
    $(".contrevenantEditionForm")
        .bootstrapValidator({
            fields: {
                contrevenant_proprietaire: {
                    validators: {
                        notEmpty: {
                            message:
                                "Le nom du propriétaire est réquis et ne peut être vide",
                        },
                    },
                },
                contrevenant_categorie: {
                    validators: {
                        notEmpty: {
                            message:
                                "La catégorie est réquise et ne peut être vide",
                        },
                    },
                },
                contrevenant_etablissement: {
                    validators: {
                        notEmpty: {
                            message:
                                "L'établissement est réquis et ne peut être vide",
                        },
                    },
                },
                contrevenant_adresse: {
                    validators: {
                        notEmpty: {
                            message:
                                "L'adresse est réquise et ne peut être vide",
                        },
                    },
                },
                contrevenant_ville: {
                    validators: {
                        notEmpty: {
                            message:
                                "La ville est réquise et ne peut être vide",
                        },
                    },
                },
            },
        })
        .on("success.form.bv", function (e) {
            // Prevent form submission
            e.preventDefault();

            var data = {
                id: $("#contrevenant-id").val(),
                proprietaire: $("#contrevenant-proprietaire").val(),
                categorie: $("#contrevenant-categorie").val(),
                etablissement: $("#contrevenant-etablissement").val(),
                adresse: $("#contrevenant-adresse").val(),
                ville: $("#contrevenant-ville").val(),
            };
            update_contrevenant(data, $("#edit-from").val());
        });
});
