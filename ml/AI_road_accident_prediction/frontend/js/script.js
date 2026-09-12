// ============================================================
// RoadSafe AI - Frontend JavaScript
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    // ------------------------------------------------------------
    // API CONFIGURATION
    // ------------------------------------------------------------

    const API_URL = "http://127.0.0.1:8000";


    // ------------------------------------------------------------
    // ELEMENTS
    // ------------------------------------------------------------

    const predictionForm =
        document.getElementById("predictionForm");

    const predictButton =
        document.getElementById("predictButton");

    const buttonText =
        document.getElementById("buttonText");

    const buttonLoader =
        document.getElementById("buttonLoader");

    const resultSection =
        document.getElementById("resultSection");

    const severityResult =
        document.getElementById("severityResult");

    const riskResult =
        document.getElementById("riskResult");

    const riskProbability =
        document.getElementById("riskProbability");

    const riskProgressBar =
        document.getElementById("riskProgressBar");

    const probabilityContainer =
        document.getElementById("probabilityContainer");

    const recommendationContainer =
        document.getElementById("recommendationContainer");

    const anotherPredictionButton =
        document.getElementById("anotherPredictionButton");


    // ------------------------------------------------------------
    // FORM SUBMIT
    // ------------------------------------------------------------

    if (predictionForm) {

        predictionForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();


                // ==================================================
                // STEP 1: VALIDATE FORM
                // ==================================================

                const validationResult =
                    validateForm();


                // If form is incomplete, STOP here
                if (!validationResult.valid) {

                    showValidationPopup(
                        validationResult.message
                    );

                    // Focus first empty field
                    if (validationResult.firstEmptyField) {

                        validationResult.firstEmptyField.focus();

                    }

                    return;
                }


                // ==================================================
                // STEP 2: START LOADING
                // ==================================================

                setLoadingState(true);


                try {

                    // ------------------------------------------------
                    // COLLECT FORM DATA
                    // ------------------------------------------------

                    const formData =
                        new FormData(predictionForm);

                    const data = {};


                    formData.forEach(
                        (value, key) => {

                            data[key] = value;

                        }
                    );


                    // ------------------------------------------------
                    // NUMBER FIELD
                    // ------------------------------------------------

                    if (
                        data.Number_of_vehicles_involved !==
                        undefined
                    ) {

                        data.Number_of_vehicles_involved =
                            Number(
                                data.Number_of_vehicles_involved
                            );

                    }


                    console.log(
                        "Sending prediction data:",
                        data
                    );


                    // ------------------------------------------------
                    // SEND DATA TO FASTAPI
                    // ------------------------------------------------

                    const response =
                        await fetch(
                            `${API_URL}/predict`,
                            {

                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(data)

                            }
                        );


                    // ------------------------------------------------
                    // CHECK SERVER RESPONSE
                    // ------------------------------------------------

                    if (!response.ok) {

                        let errorMessage =
                            `Server error: ${response.status}`;


                        try {

                            const errorData =
                                await response.json();


                            if (errorData.detail) {

                                errorMessage =
                                    typeof errorData.detail ===
                                        "string"
                                        ? errorData.detail
                                        : JSON.stringify(
                                            errorData.detail
                                        );

                            }

                        } catch (error) {

                            console.error(
                                "Could not read server error:",
                                error
                            );

                        }


                        throw new Error(
                            errorMessage
                        );

                    }


                    // ------------------------------------------------
                    // GET RESULT
                    // ------------------------------------------------

                    const result =
                        await response.json();


                    console.log(
                        "Prediction response:",
                        result
                    );


                    // ------------------------------------------------
                    // DISPLAY RESULT
                    // ------------------------------------------------

                    displayPredictionResult(
                        result
                    );


                } catch (error) {

                    console.error(
                        "Prediction error:",
                        error
                    );


                    showError(
                        error.message ||
                        "Unable to connect to the prediction server."
                    );


                } finally {

                    setLoadingState(false);

                }

            }
        );

    }


    // ============================================================
    // FORM VALIDATION
    // ============================================================

    function validateForm() {

        /*
         * These are the exact fields used by your backend.
         */

        const requiredFields = [

            "Time",
            "Day_of_week",
            "Age_band_of_driver",
            "Sex_of_driver",
            "Educational_level",
            "Vehicle_driver_relation",
            "Driving_experience",

            "Type_of_vehicle",
            "Owner_of_vehicle",
            "Service_year_of_vehicle",
            "Defect_of_vehicle",
            "Number_of_vehicles_involved",

            "Area_accident_occured",
            "Lanes_or_Medians",
            "Road_allignment",
            "Types_of_Junction",
            "Road_surface_type",
            "Road_surface_conditions",
            "Vehicle_movement",

            "Light_conditions",
            "Weather_conditions",
            "Type_of_collision"

        ];


        let firstEmptyField = null;


        // ----------------------------------------------------------
        // REMOVE OLD ERROR STYLING
        // ----------------------------------------------------------

        requiredFields.forEach(
            (fieldName) => {

                const field =
                    predictionForm.elements[fieldName];


                if (field) {

                    field.classList.remove(
                        "input-error"
                    );

                }

            }
        );


        // ----------------------------------------------------------
        // CHECK EVERY REQUIRED FIELD
        // ----------------------------------------------------------

        for (
            const fieldName of requiredFields
        ) {

            const field =
                predictionForm.elements[fieldName];


            if (!field) {
                continue;
            }


            let value =
                field.value;


            // Trim text values
            if (typeof value === "string") {
                value = value.trim();
            }


            // Empty field
            if (!value) {

                field.classList.add(
                    "input-error"
                );


                if (!firstEmptyField) {

                    firstEmptyField =
                        field;

                }

            }

        }


        // ----------------------------------------------------------
        // IF SOMETHING IS EMPTY
        // ----------------------------------------------------------

        if (firstEmptyField) {

            return {

                valid: false,

                message:
                    "Please fill in all required fields before analyzing the accident risk.",

                firstEmptyField:
                    firstEmptyField

            };

        }


        // ----------------------------------------------------------
        // EVERYTHING IS FILLED
        // ----------------------------------------------------------

        return {

            valid: true,

            message: "",

            firstEmptyField: null

        };

    }


    // ============================================================
    // VALIDATION POPUP
    // ============================================================

    function showValidationPopup(message) {

        // Remove existing popup
        const existingPopup =
            document.querySelector(
                ".validation-popup"
            );


        if (existingPopup) {
            existingPopup.remove();
        }


        // ----------------------------------------------------------
        // CREATE POPUP
        // ----------------------------------------------------------

        const popup =
            document.createElement("div");

        popup.className =
            "validation-popup";


        popup.innerHTML = `

            <div class="validation-popup-box">

                <div class="validation-popup-icon">
                    !
                </div>

                <div class="validation-popup-content">

                    <h3>
                        Input Required
                    </h3>

                    <p>
                        ${message}
                    </p>

                </div>

                <button
                    type="button"
                    class="validation-popup-close"
                    aria-label="Close"
                >
                    ×
                </button>

            </div>

        `;


        document.body.appendChild(
            popup
        );


        // ----------------------------------------------------------
        // CLOSE BUTTON
        // ----------------------------------------------------------

        const closeButton =
            popup.querySelector(
                ".validation-popup-close"
            );


        closeButton.addEventListener(
            "click",
            () => {

                popup.remove();

            }
        );


        // ----------------------------------------------------------
        // CLICK OUTSIDE POPUP
        // ----------------------------------------------------------

        popup.addEventListener(
            "click",
            (event) => {

                if (
                    event.target === popup
                ) {

                    popup.remove();

                }

            }
        );


        // ----------------------------------------------------------
        // AUTO CLOSE
        // ----------------------------------------------------------

        setTimeout(
            () => {

                if (popup) {
                    popup.remove();
                }

            },
            5000
        );

    }


    // ============================================================
    // REMOVE ERROR WHEN USER FILLS FIELD
    // ============================================================

    const formInputs =
        predictionForm
            ? predictionForm.querySelectorAll(
                "input, select, textarea"
            )
            : [];


    formInputs.forEach(
        (input) => {

            input.addEventListener(
                "change",
                () => {

                    if (input.value) {

                        input.classList.remove(
                            "input-error"
                        );

                    }

                }
            );


            input.addEventListener(
                "input",
                () => {

                    if (input.value.trim()) {

                        input.classList.remove(
                            "input-error"
                        );

                    }

                }
            );

        }
    );


    // ============================================================
    // DISPLAY PREDICTION RESULT
    // ============================================================

    function displayPredictionResult(result) {

        const prediction =
            result.prediction || result;


        // ----------------------------------------------------------
        // SEVERITY
        // ----------------------------------------------------------

        const severity =
            prediction.severity ||
            prediction.Severity ||
            prediction.accident_severity ||
            "Unknown";


        // ----------------------------------------------------------
        // RISK LEVEL
        // ----------------------------------------------------------

        const riskLevel =
            prediction.risk_level ||
            prediction.riskLevel ||
            prediction.risk ||
            "Unknown";


        // ----------------------------------------------------------
        // RISK SCORE
        // ----------------------------------------------------------

        let riskScore =
            prediction.risk_score ??
            prediction.riskScore ??
            prediction.probability ??
            prediction.risk_probability ??
            0;


        riskScore =
            Number(riskScore);


        // Convert decimal to percentage
        if (
            riskScore > 0 &&
            riskScore <= 1
        ) {

            riskScore =
                riskScore * 100;

        }


        riskScore =
            Math.max(
                0,
                Math.min(
                    100,
                    riskScore
                )
            );


        // ----------------------------------------------------------
        // SEVERITY RESULT
        // ----------------------------------------------------------

        if (severityResult) {

            severityResult.textContent =
                formatText(severity);

        }


        // ----------------------------------------------------------
        // RISK RESULT
        // ----------------------------------------------------------

        if (riskResult) {

            riskResult.textContent =
                formatText(riskLevel);


            riskResult.classList.remove(
                "risk-low",
                "risk-medium",
                "risk-high"
            );


            const normalizedRisk =
                String(
                    riskLevel
                ).toLowerCase();


            if (
                normalizedRisk.includes("low") ||
                normalizedRisk.includes("safe")
            ) {

                riskResult.classList.add(
                    "risk-low"
                );

            } else if (
                normalizedRisk.includes("medium") ||
                normalizedRisk.includes("moderate")
            ) {

                riskResult.classList.add(
                    "risk-medium"
                );

            } else if (
                normalizedRisk.includes("high") ||
                normalizedRisk.includes("danger")
            ) {

                riskResult.classList.add(
                    "risk-high"
                );

            }

        }


        // ----------------------------------------------------------
        // RISK PERCENTAGE
        // ----------------------------------------------------------

        if (riskProbability) {

            riskProbability.textContent =
                `${riskScore.toFixed(1)}%`;

        }


        // ----------------------------------------------------------
        // PROGRESS BAR
        // ----------------------------------------------------------

        if (riskProgressBar) {

            riskProgressBar.style.width =
                "0%";


            setTimeout(
                () => {

                    riskProgressBar.style.width =
                        `${riskScore}%`;

                },
                100
            );

        }


        // ----------------------------------------------------------
        // PROBABILITIES
        // ----------------------------------------------------------

        displayProbabilities(
            prediction.probabilities
        );


        // ----------------------------------------------------------
        // RECOMMENDATIONS
        // ----------------------------------------------------------

        displayRecommendations(
            prediction.recommendations
        );


        // ----------------------------------------------------------
        // SHOW RESULT
        // ----------------------------------------------------------

        if (resultSection) {

            resultSection.classList.remove(
                "hidden"
            );


            resultSection.classList.remove(
                "result-visible"
            );


            setTimeout(
                () => {

                    resultSection.classList.add(
                        "result-visible"
                    );

                },
                50
            );


            setTimeout(
                () => {

                    resultSection.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                },
                150
            );

        }

    }


    // ============================================================
    // DISPLAY PROBABILITIES
    // ============================================================

    function displayProbabilities(
        probabilities
    ) {

        if (!probabilityContainer) {
            return;
        }


        probabilityContainer.innerHTML =
            "";


        if (
            !probabilities ||
            typeof probabilities !== "object"
        ) {

            probabilityContainer.innerHTML = `

                <div class="empty-result">
                    Probability details are not available.
                </div>

            `;

            return;

        }


        const probabilityEntries =
            Object.entries(
                probabilities
            );


        probabilityEntries.sort(
            (a, b) =>
                Number(b[1]) -
                Number(a[1])
        );


        probabilityEntries.forEach(
            ([label, value]) => {

                let percentage =
                    Number(value);


                if (
                    percentage >= 0 &&
                    percentage <= 1
                ) {

                    percentage *= 100;

                }


                percentage =
                    Math.max(
                        0,
                        Math.min(
                            100,
                            percentage
                        )
                    );


                const item =
                    document.createElement(
                        "div"
                    );


                item.className =
                    "probability-item";


                item.innerHTML = `

                    <div class="probability-header">

                        <span class="probability-label">
                            ${formatText(label)}
                        </span>

                        <span class="probability-value">
                            ${percentage.toFixed(1)}%
                        </span>

                    </div>

                    <div class="probability-bar">

                        <div
                            class="probability-fill"
                            style="width: 0%"
                        ></div>

                    </div>

                `;


                probabilityContainer.appendChild(
                    item
                );


                const fill =
                    item.querySelector(
                        ".probability-fill"
                    );


                setTimeout(
                    () => {

                        if (fill) {

                            fill.style.width =
                                `${percentage}%`;

                        }

                    },
                    100
                );

            }
        );

    }


    // ============================================================
    // DISPLAY RECOMMENDATIONS
    // ============================================================

    function displayRecommendations(
        recommendations
    ) {

        if (!recommendationContainer) {
            return;
        }


        recommendationContainer.innerHTML =
            "";


        if (!recommendations) {

            recommendationContainer.innerHTML = `

                <div class="recommendation-item">

                    <span class="recommendation-icon">
                        ✓
                    </span>

                    <span class="recommendation-text">
                        Drive safely and follow all traffic rules.
                    </span>

                </div>

            `;

            return;

        }


        if (
            typeof recommendations ===
            "string"
        ) {

            recommendations = [
                recommendations
            ];

        }


        if (
            !Array.isArray(
                recommendations
            )
        ) {

            recommendations = [
                String(recommendations)
            ];

        }


        recommendations.forEach(
            (recommendation, index) => {

                const item =
                    document.createElement(
                        "div"
                    );


                item.className =
                    "recommendation-item";


                item.innerHTML = `

                    <span class="recommendation-icon">
                        ${index + 1}
                    </span>

                    <span class="recommendation-text">
                        ${formatText(
                    recommendation
                )}
                    </span>

                `;


                recommendationContainer.appendChild(
                    item
                );

            }
        );

    }


    // ============================================================
    // LOADING STATE
    // ============================================================

    function setLoadingState(
        isLoading
    ) {

        if (!predictButton) {
            return;
        }


        if (isLoading) {

            predictButton.disabled =
                true;


            predictButton.classList.add(
                "loading"
            );


            if (buttonText) {

                buttonText.textContent =
                    "Analyzing...";

            }


            if (buttonLoader) {

                buttonLoader.classList.remove(
                    "hidden"
                );

            }

        } else {

            predictButton.disabled =
                false;


            predictButton.classList.remove(
                "loading"
            );


            if (buttonText) {

                buttonText.textContent =
                    "Analyze Accident Risk";

            }


            if (buttonLoader) {

                buttonLoader.classList.add(
                    "hidden"
                );

            }

        }

    }


    // ============================================================
    // ERROR MESSAGE
    // ============================================================

    function showError(
        message
    ) {

        if (resultSection) {

            resultSection.classList.add(
                "hidden"
            );

        }


        const oldError =
            document.querySelector(
                ".prediction-error"
            );


        if (oldError) {
            oldError.remove();
        }


        const errorBox =
            document.createElement(
                "div"
            );


        errorBox.className =
            "prediction-error";


        errorBox.innerHTML = `

            <div class="error-icon">
                !
            </div>

            <div class="error-content">

                <strong>
                    Prediction Error
                </strong>

                <p>
                    ${formatText(message)}
                </p>

                <small>
                    Make sure your FastAPI backend is running
                    at http://127.0.0.1:8000
                </small>

            </div>

        `;


        predictionForm.parentNode.insertBefore(
            errorBox,
            predictionForm
        );


        setTimeout(
            () => {

                if (errorBox) {
                    errorBox.remove();
                }

            },
            8000
        );

    }


    // ============================================================
    // MAKE ANOTHER PREDICTION
    //
    // NOW IT CLEARS ALL OLD INPUTS
    // ============================================================

    if (anotherPredictionButton) {

        anotherPredictionButton.addEventListener(
            "click",
            (event) => {

                event.preventDefault();


                // --------------------------------------------------
                // HIDE RESULT
                // --------------------------------------------------

                if (resultSection) {

                    resultSection.classList.add(
                        "hidden"
                    );

                }


                // --------------------------------------------------
                // CLEAR FORM
                // --------------------------------------------------

                if (predictionForm) {

                    predictionForm.reset();

                }


                // --------------------------------------------------
                // REMOVE ALL ERROR HIGHLIGHTS
                // --------------------------------------------------

                const fields =
                    predictionForm.querySelectorAll(
                        "input, select, textarea"
                    );


                fields.forEach(
                    (field) => {

                        field.classList.remove(
                            "input-error"
                        );

                    }
                );


                // --------------------------------------------------
                // CLEAR OLD RESULT DATA
                // --------------------------------------------------

                if (severityResult) {
                    severityResult.textContent =
                        "";
                }


                if (riskResult) {

                    riskResult.textContent =
                        "";

                    riskResult.classList.remove(
                        "risk-low",
                        "risk-medium",
                        "risk-high"
                    );

                }


                if (riskProbability) {

                    riskProbability.textContent =
                        "0%";

                }


                if (riskProgressBar) {

                    riskProgressBar.style.width =
                        "0%";

                }


                if (probabilityContainer) {

                    probabilityContainer.innerHTML =
                        "";

                }


                if (recommendationContainer) {

                    recommendationContainer.innerHTML =
                        "";

                }


                // --------------------------------------------------
                // SCROLL TO FORM
                // --------------------------------------------------

                const predictionSection =
                    document.getElementById(
                        "prediction"
                    );


                if (predictionSection) {

                    predictionSection.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }

            }
        );

    }


    // ============================================================
    // MOBILE MENU
    // ============================================================

    const menuToggle =
        document.querySelector(
            ".menu-toggle"
        );

    const navLinks =
        document.querySelector(
            ".nav-links"
        );


    if (
        menuToggle &&
        navLinks
    ) {

        menuToggle.addEventListener(
            "click",
            () => {

                navLinks.classList.toggle(
                    "active"
                );

                menuToggle.classList.toggle(
                    "active"
                );

            }
        );


        navLinks
            .querySelectorAll("a")
            .forEach(
                (link) => {

                    link.addEventListener(
                        "click",
                        () => {

                            navLinks.classList.remove(
                                "active"
                            );

                            menuToggle.classList.remove(
                                "active"
                            );

                        }
                    );

                }
            );

    }


    // ============================================================
    // SMOOTH SCROLL
    // ============================================================

    document
        .querySelectorAll(
            'a[href^="#"]'
        )
        .forEach(
            (link) => {

                link.addEventListener(
                    "click",
                    (event) => {

                        const targetId =
                            link.getAttribute(
                                "href"
                            );


                        if (
                            !targetId ||
                            targetId === "#"
                        ) {

                            return;

                        }


                        const target =
                            document.querySelector(
                                targetId
                            );


                        if (target) {

                            event.preventDefault();


                            target.scrollIntoView({
                                behavior:
                                    "smooth",
                                block:
                                    "start"
                            });

                        }

                    }
                );

            }
        );


    // ============================================================
    // INPUT FOCUS
    // ============================================================

    const inputs =
        document.querySelectorAll(
            "input, select, textarea"
        );


    inputs.forEach(
        (input) => {

            input.addEventListener(
                "focus",
                () => {

                    input.parentElement?.classList.add(
                        "input-focused"
                    );

                }
            );


            input.addEventListener(
                "blur",
                () => {

                    input.parentElement?.classList.remove(
                        "input-focused"
                    );

                }
            );

        }
    );


    // ============================================================
    // FORMAT TEXT
    // ============================================================

    function formatText(value) {

        if (
            value === null ||
            value === undefined
        ) {

            return "";

        }


        let text =
            String(value);


        text =
            text.replace(
                /_/g,
                " "
            );


        text =
            text.replace(
                /-/g,
                " "
            );


        text =
            text.replace(
                /\s+/g,
                " "
            )
                .trim();


        text =
            text.replace(
                /\b\w/g,
                (letter) =>
                    letter.toUpperCase()
            );


        return text;

    }


    // ============================================================
    // INITIAL STATE
    // ============================================================

    if (resultSection) {

        resultSection.classList.add(
            "hidden"
        );

    }


    if (buttonLoader) {

        buttonLoader.classList.add(
            "hidden"
        );

    }


    console.log(
        "RoadSafe AI frontend initialized successfully."
    );

});
