var etablissements = [];
var quickSeacrhResult = [];
$("#quick-search-submit").click(function (e) {
    e.preventDefault();
    var date_du = $("#date_du");
    var date_au = $("#date_au");
    var etablissement_autocomplete = $("#etablissement_autocomplete");
    if (date_du.val() === "") {
        date_du.addClass("is-invalid");
        return;
    } else {
        if (date_du.hasClass("is-invalid")) date_du.removeClass("is-invalid");
    }
    if (date_au.val() === "") {
        date_au.addClass("is-invalid");
        return;
    } else {
        if (date_au.hasClass("is-invalid")) date_au.removeClass("is-invalid");
    }

    if (
        etablissement_autocomplete.val() === "" ||
        !etablissements.find((x) => x === etablissement_autocomplete.val().trim())
    ) {
        etablissement_autocomplete.addClass("is-invalid");
        return;
    } else {
        if (etablissement_autocomplete.hasClass("is-invalid"))
            etablissement_autocomplete.removeClass("is-invalid");
    }

    var alert_qck_search = $("#alert-error-qck-search");
    if (date_du.val() > date_au.val()) {
        alert_qck_search.removeClass("hidden");
    } else {
        if (!alert_qck_search.hasClass("hidden")) {
            alert_qck_search.addClass("hidden");
            return;
        }
    }

    fetch(
        `${
            window.location.origin
        }/contrevenants?du=${date_du.val()}&au=${date_au.val()}&etablissement=${etablissement_autocomplete.val()}`
    )
        .then(function (data) {
            data.json().then(function (response) {
                quickSeacrhResult = response;
                fill_qck_search_table(quickSeacrhResult);
            });
        })
        .catch(function (error) {
            console.log(error);
        });
});

function fill_qck_search_table(quickSeacrhResult) {
    $("#quick-search-result tbody").empty();
    var html = "";
    quickSeacrhResult.forEach((elt, index) => {
        html += `<tr>
                    <td scope="row">${elt.date_infraction}</td>
                    <td scope="row" class="parentCell">${elt.description.slice(
            0,
            100
        )}...
                        <span class="tooltip1">${elt.description}</span>
                    </td>
                    <td scope="row">${elt.date_jugement}</td>
                    <td scope="row">${elt.montant}</td>
                 </tr>`;
    });
    $("#quick-search-result tbody:last-child").append(html);

    getPagination("#quick-search-result");
}

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
                    if (from !== "qck-search") {
                        location.reload();
                    } else {
                        quickSeacrhResult.forEach((elt) => {
                            if (elt.id == data.id) {
                                (elt.description = data.description),
                                    (elt.date_jugement = data.date_jugement),
                                    (elt.montant = `${data.montant} $`);
                            }
                        });
                        fill_qck_search_table(quickSeacrhResult);
                        $("#edit_contrevenant").modal("hide");
                    }
                },
            });
            if (!response.ok) {
                Toast.fire({
                    icon: "error",
                    title: "Signed in successfully",
                });
            } else
                Toast.fire({
                    icon: "success",
                    title: "Signed in successfully",
                });
        })
        .catch((data) => {
            console.log(data);
        });
}

function fill_etablissements_select() {
    fetch(`${window.location.origin}/contrevenants/etablissements`)
        .then((response) => {
            if (response.ok) {
                response.json().then((data) => {
                    etablissements = data;
                    autocomplete(
                        document.getElementById("etablissement_autocomplete"),
                        data
                    );
                });
            }
        })
        .catch((error) => {
            console.log(`Request failed: ${error}`);
        });
}
