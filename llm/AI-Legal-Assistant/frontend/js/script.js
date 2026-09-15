const API_BASE_URL = "http://127.0.0.1:8000";

let currentDocumentId = null;
let selectedFile = null;

const documentInput = document.getElementById("documentInput");
const chooseFileButton = document.getElementById("chooseFileButton");
const uploadBox = document.getElementById("uploadBox");
const selectedFileBox = document.getElementById("selectedFile");
const selectedFileName = document.getElementById("selectedFileName");
const selectedFileSize = document.getElementById("selectedFileSize");
const removeFileButton = document.getElementById("removeFileButton");
const uploadButton = document.getElementById("uploadButton");

const documentInfo = document.getElementById("documentInfo");

const infoFileName = document.getElementById("infoFileName");
const infoFileType = document.getElementById("infoFileType");
const infoFileSize = document.getElementById("infoFileSize");
const infoWordCount = document.getElementById("infoWordCount");
const infoChunkCount = document.getElementById("infoChunkCount");
const infoEmbeddingDimension = document.getElementById("infoEmbeddingDimension");

const summaryButton = document.getElementById("summaryButton");
const chatFeatureButton = document.getElementById("chatFeatureButton");
const rightsButton = document.getElementById("rightsButton");
const riskButton = document.getElementById("riskButton");
const recommendationButton = document.getElementById("recommendationButton");

const resultsSection = document.getElementById("results");
const resultTitle = document.getElementById("resultTitle");
const resultContent = document.getElementById("resultContent");
const clearResultButton = document.getElementById("clearResultButton");

const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const sendChatButton = document.getElementById("sendChatButton");

const loadingOverlay = document.getElementById("loadingOverlay");
const loadingTitle = document.getElementById("loadingTitle");
const loadingMessage = document.getElementById("loadingMessage");

const toast = document.getElementById("toast");
const toastTitle = document.getElementById("toastTitle");
const toastMessage = document.getElementById("toastMessage");
const toastClose = document.getElementById("toastClose");

console.log("[AI Legal Assistant] script.js loaded successfully");
console.log("[AI Legal Assistant] API Base URL:", API_BASE_URL);


/* =========================================================
   FILE PICKER
========================================================= */

if (chooseFileButton && documentInput) {

    chooseFileButton.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        console.log("[AI Legal Assistant] Choose Document button clicked");

        documentInput.click();

    });

}


if (uploadBox && documentInput) {

    uploadBox.addEventListener("click", function (event) {

        if (event.target === chooseFileButton) {
            return;
        }

        if (
            event.target.closest(".remove-file-button") ||
            event.target.closest(".upload-button")
        ) {
            return;
        }

        console.log("[AI Legal Assistant] Upload box clicked");

        documentInput.click();

    });

}


if (documentInput) {

    documentInput.addEventListener("change", function (event) {

        console.log(
            "[AI Legal Assistant] File input changed:",
            event.target.files
        );

        if (!event.target.files || event.target.files.length === 0) {
            return;
        }

        handleSelectedFile(event.target.files[0]);

    });

}


/* =========================================================
   FILE VALIDATION
========================================================= */

function handleSelectedFile(file) {

    console.log("[AI Legal Assistant] Handling file:", file);

    const allowedExtensions = [".pdf", ".docx", ".txt"];
    const fileName = file.name.toLowerCase();

    const isAllowed = allowedExtensions.some(function (extension) {
        return fileName.endsWith(extension);
    });

    if (!isAllowed) {

        showToast(
            "Invalid File",
            "Only PDF, DOCX and TXT files are allowed."
        );

        resetFileSelection();

        return;
    }


    const maxFileSize = 20 * 1024 * 1024;

    if (file.size > maxFileSize) {

        showToast(
            "File Too Large",
            "Maximum allowed file size is 20 MB."
        );

        resetFileSelection();

        return;
    }


    if (file.size === 0) {

        showToast(
            "Empty File",
            "Please select a document containing legal content."
        );

        resetFileSelection();

        return;
    }


    selectedFile = file;

    selectedFileName.textContent = file.name;
    selectedFileSize.textContent = formatFileSize(file.size);

    if (selectedFileBox) {
        selectedFileBox.style.display = "flex";
    }

    if (uploadBox) {
        uploadBox.classList.add("has-file");
    }

    if (uploadButton) {
        uploadButton.disabled = false;
    }

    console.log("[AI Legal Assistant] File selected successfully:", file.name);

    showToast(
        "File Selected",
        "Your document is ready to upload."
    );

}


/* =========================================================
   FILE SIZE
========================================================= */

function formatFileSize(bytes) {

    if (bytes === 0) {
        return "0 Bytes";
    }

    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];

    const index = Math.floor(
        Math.log(bytes) / Math.log(1024)
    );

    return (
        parseFloat(
            (bytes / Math.pow(1024, index)).toFixed(2)
        ) +
        " " +
        units[index]
    );

}


/* =========================================================
   REMOVE FILE
========================================================= */

if (removeFileButton) {

    removeFileButton.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        resetFileSelection();

    });

}


function resetFileSelection() {

    selectedFile = null;

    if (documentInput) {
        documentInput.value = "";
    }

    if (selectedFileBox) {
        selectedFileBox.style.display = "none";
    }

    if (uploadBox) {
        uploadBox.classList.remove("has-file");
    }

    if (uploadButton) {
        uploadButton.disabled = true;
    }

    console.log("[AI Legal Assistant] File selection reset");

}


/* =========================================================
   UPLOAD DOCUMENT
========================================================= */

if (uploadButton) {

    uploadButton.addEventListener("click", async function (event) {

        event.preventDefault();
        event.stopPropagation();

        if (!selectedFile) {

            showToast(
                "No Document",
                "Please choose a document first."
            );

            return;
        }

        await uploadDocument();

    });

}


async function uploadDocument() {

    if (!selectedFile) {
        return;
    }


    const formData = new FormData();

    formData.append("file", selectedFile);


    setLoading(
        true,
        "Uploading Document",
        "The document is being processed and indexed. Please wait."
    );


    if (uploadButton) {
        uploadButton.disabled = true;
    }


    try {

        console.log(
            "[AI Legal Assistant] Uploading document:",
            selectedFile.name
        );


        const response = await fetch(
            `${API_BASE_URL} /documents/upload`,
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        console.log(
            "[AI Legal Assistant] Upload response:",
            data
        );


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Document upload failed."
            );

        }


        currentDocumentId = data.document_id;


        localStorage.setItem(
            "currentDocumentId",
            currentDocumentId
        );


        displayDocumentInformation(data);

        enableFeatures();

        resetFileSelection();


        showToast(
            "Upload Successful",
            "Your document has been processed successfully."
        );


        addAssistantMessage(
            "Your document has been uploaded and indexed successfully. You can now ask questions or use the analysis features."
        );


    } catch (error) {

        console.error(
            "[AI Legal Assistant] Upload error:",
            error
        );


        showToast(
            "Upload Failed",
            error.message || "Could not upload the document."
        );


        if (uploadButton) {
            uploadButton.disabled = false;
        }


    } finally {

        setLoading(false);

    }

}


/* =========================================================
   DOCUMENT INFORMATION
========================================================= */

function displayDocumentInformation(data) {

    if (!documentInfo) {
        return;
    }


    documentInfo.style.display = "block";


    if (infoFileName) {
        infoFileName.textContent =
            data.filename || "-";
    }


    if (infoFileType) {
        infoFileType.textContent =
            data.file_type
                ? data.file_type.replace(".", "").toUpperCase()
                : "-";
    }


    if (infoFileSize) {
        infoFileSize.textContent =
            data.file_size
                ? formatFileSize(data.file_size)
                : "-";
    }


    if (infoWordCount) {
        infoWordCount.textContent =
            data.word_count ?? "-";
    }


    if (infoChunkCount) {
        infoChunkCount.textContent =
            data.chunk_count ?? "-";
    }


    if (infoEmbeddingDimension) {
        infoEmbeddingDimension.textContent =
            data.embedding_dimension ?? "-";
    }

}


/* =========================================================
   ENABLE FEATURES
========================================================= */

function enableFeatures() {

    const buttons = [
        summaryButton,
        chatFeatureButton,
        rightsButton,
        riskButton,
        recommendationButton
    ];


    buttons.forEach(function (button) {

        if (button) {
            button.disabled = false;
        }

    });


    if (chatInput) {
        chatInput.disabled = false;
    }


    if (sendChatButton) {
        sendChatButton.disabled = false;
    }


    console.log(
        "[AI Legal Assistant] Features enabled"
    );

}


/* =========================================================
   RESTORE CURRENT DOCUMENT
========================================================= */

const savedDocumentId =
    localStorage.getItem("currentDocumentId");


if (savedDocumentId) {

    currentDocumentId = savedDocumentId;

    console.log(
        "[AI Legal Assistant] Saved document ID:",
        currentDocumentId
    );

}


/* =========================================================
   SUMMARY
========================================================= */

if (summaryButton) {

    summaryButton.addEventListener(
        "click",
        async function () {

            await generateSummary();

        }
    );

}


async function generateSummary() {

    if (!currentDocumentId) {

        showToast(
            "No Document",
            "Please upload a document first."
        );

        return;
    }


    setLoading(
        true,
        "Generating Summary",
        "The AI is simplifying your legal document."
    );


    try {

        const response = await fetch(
            `${API_BASE_URL} /documents/summary`,
            {
                method: "POST"
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Could not generate the summary."
            );

        }


        showResult(
            "Document Summary",
            data.summary || "No summary was generated."
        );


    } catch (error) {

        console.error(
            "[AI Legal Assistant] Summary error:",
            error
        );


        showToast(
            "Summary Failed",
            error.message
        );


    } finally {

        setLoading(false);

    }

}


/* =========================================================
   RIGHTS & OBLIGATIONS
========================================================= */

if (rightsButton) {

    rightsButton.addEventListener(
        "click",
        async function () {

            await analyzeRights();

        }
    );

}


async function analyzeRights() {

    if (!currentDocumentId) {

        showToast(
            "No Document",
            "Please upload a document first."
        );

        return;
    }


    setLoading(
        true,
        "Analyzing Rights",
        "The AI is identifying rights and obligations in the document."
    );


    try {

        const response = await fetch(
            `${API_BASE_URL} /rights/analyze`,
            {
                method: "GET"
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Rights analysis failed."
            );

        }


        showResult(
            "Rights & Obligations",
            data.analysis || "No rights analysis was generated."
        );


    } catch (error) {

        console.error(
            "[AI Legal Assistant] Rights error:",
            error
        );


        showToast(
            "Rights Analysis Failed",
            error.message
        );


    } finally {

        setLoading(false);

    }

}


/* =========================================================
   RISK ANALYSIS
========================================================= */

if (riskButton) {

    riskButton.addEventListener(
        "click",
        async function () {

            await analyzeRisks();

        }
    );

}


async function analyzeRisks() {

    if (!currentDocumentId) {

        showToast(
            "No Document",
            "Please upload a document first."
        );

        return;
    }


    setLoading(
        true,
        "Analyzing Risks",
        "The AI is analyzing the document for potentially important risks."
    );


    try {

        const response = await fetch(
            `${API_BASE_URL} /risks/analyze`,
            {
                method: "GET"
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Risk analysis failed."
            );

        }


        showResult(
            "Risk Analysis",
            data.analysis || "No risk analysis was generated."
        );


    } catch (error) {

        console.error(
            "[AI Legal Assistant] Risk error:",
            error
        );


        showToast(
            "Risk Analysis Failed",
            error.message
        );


    } finally {

        setLoading(false);

    }

}


/* =========================================================
   RECOMMENDATIONS
========================================================= */

if (recommendationButton) {

    recommendationButton.addEventListener(
        "click",
        async function () {

            await getRecommendations();

        }
    );

}


async function getRecommendations() {

    if (!currentDocumentId) {

        showToast(
            "No Document",
            "Please upload a document first."
        );

        return;
    }


    setLoading(
        true,
        "Generating Recommendations",
        "The AI is preparing recommendations based on your document."
    );


    try {

        const response = await fetch(
            `${API_BASE_URL} /recommendations/analyze`,
            {
                method: "GET"
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Recommendation generation failed."
            );

        }


        showResult(
            "Recommendations",
            data.analysis || "No recommendations were generated."
        );


    } catch (error) {

        console.error(
            "[AI Legal Assistant] Recommendation error:",
            error
        );


        showToast(
            "Recommendation Failed",
            error.message
        );


    } finally {

        setLoading(false);

    }

}


/* =========================================================
   SHOW RESULT
========================================================= */

function showResult(title, content) {

    if (!resultsSection || !resultTitle || !resultContent) {
        return;
    }


    resultTitle.textContent = title;


    resultContent.innerHTML =
        formatAIResponse(content);


    resultsSection.style.display = "block";


    setTimeout(function () {

        resultsSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }, 100);

}


/* =========================================================
   CLEAR RESULT
========================================================= */

if (clearResultButton) {

    clearResultButton.addEventListener(
        "click",
        function () {

            if (resultsSection) {
                resultsSection.style.display = "none";
            }

            if (resultContent) {
                resultContent.innerHTML = "";
            }

        }
    );

}


/* =========================================================
   CHAT FEATURE BUTTON
========================================================= */

if (chatFeatureButton) {

    chatFeatureButton.addEventListener(
        "click",
        function () {

            if (!currentDocumentId) {

                showToast(
                    "No Document",
                    "Please upload a document first."
                );

                return;
            }


            const chatSection =
                document.getElementById("chat");


            if (chatSection) {

                chatSection.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }


            if (chatInput) {

                setTimeout(function () {

                    chatInput.focus();

                }, 500);

            }

        }
    );

}


/* =========================================================
   CHAT SEND
========================================================= */

if (sendChatButton) {

    sendChatButton.addEventListener(
        "click",
        async function () {

            await sendChatMessage();

        }
    );

}


if (chatInput) {

    chatInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendChatMessage();

            }

        }
    );

}


async function sendChatMessage() {

    if (!currentDocumentId) {

        showToast(
            "No Document",
            "Please upload a document first."
        );

        return;
    }


    const question =
        chatInput.value.trim();


    if (!question) {

        showToast(
            "Enter a Question",
            "Please type a question about your document."
        );

        chatInput.focus();

        return;
    }


    addUserMessage(question);


    chatInput.value = "";


    setChatLoading(true);


    try {

        const response = await fetch(
            `${API_BASE_URL} /chat/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Could not get an answer."
            );

        }


        const answer =
            data.answer ||
            data.response ||
            data.message ||
            "I could not find a clear answer in the provided document.";


        addAssistantMessage(answer);


    } catch (error) {

        console.error(
            "[AI Legal Assistant] Chat error:",
            error
        );


        addAssistantMessage(
            "Sorry, I could not process your question. " +
            (error.message || "")
        );


    } finally {

        setChatLoading(false);

    }

}


/* =========================================================
   ADD USER MESSAGE
========================================================= */

function addUserMessage(message) {

    if (!chatMessages) {
        return;
    }


    const messageElement =
        document.createElement("div");


    messageElement.className =
        "chat-message user-message";


    messageElement.innerHTML = `
    < div class="message-label" >
        You
        </div >

    <div class="message-text">
        ${escapeHTML(message)}
    </div>
`;


    chatMessages.appendChild(messageElement);


    scrollChatToBottom();

}


/* =========================================================
   ADD ASSISTANT MESSAGE
========================================================= */

function addAssistantMessage(message) {

    if (!chatMessages) {
        return;
    }


    const messageElement =
        document.createElement("div");


    messageElement.className =
        "chat-message assistant-message";


    messageElement.innerHTML = `
    < div class="message-label" >
        AI Assistant
        </div >

    <div class="message-text">
        ${formatAIResponse(message)}
    </div>
`;


    chatMessages.appendChild(messageElement);


    scrollChatToBottom();

}


/* =========================================================
   CHAT SCROLL
========================================================= */

function scrollChatToBottom() {

    if (!chatMessages) {
        return;
    }


    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


/* =========================================================
   CHAT LOADING
========================================================= */

function setChatLoading(isLoading) {

    if (sendChatButton) {
        sendChatButton.disabled = isLoading;
    }


    if (chatInput) {
        chatInput.disabled = isLoading;
    }


    if (!chatMessages) {
        return;
    }


    const existingLoader =
        document.getElementById("chatTypingLoader");


    if (isLoading) {

        if (existingLoader) {
            return;
        }


        const loader =
            document.createElement("div");


        loader.id =
            "chatTypingLoader";


        loader.className =
            "chat-message assistant-message";


        loader.innerHTML = `
    < div class="message-label" >
        AI Assistant
            </div >

    <div class="message-text">
        Thinking...
    </div>
`;


        chatMessages.appendChild(loader);


        scrollChatToBottom();


    } else {

        if (existingLoader) {
            existingLoader.remove();
        }

    }

}


/* =========================================================
   FORMAT AI RESPONSE
========================================================= */

function formatAIResponse(text) {

    if (!text) {
        return "";
    }


    let safeText =
        escapeHTML(String(text));


    safeText =
        safeText.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    safeText =
        safeText.replace(
            /\n/g,
            "<br>"
        );


    return safeText;

}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(text) {

    const element =
        document.createElement("div");


    element.textContent = text;


    return element.innerHTML;

}


/* =========================================================
   LOADING OVERLAY
========================================================= */

function setLoading(
    isLoading,
    title = "Processing...",
    message = "Please wait while the AI processes your request."
) {

    if (!loadingOverlay) {
        return;
    }


    if (isLoading) {

        loadingOverlay.style.display =
            "flex";


        if (loadingTitle) {
            loadingTitle.textContent =
                title;
        }


        if (loadingMessage) {
            loadingMessage.textContent =
                message;
        }


    } else {

        loadingOverlay.style.display =
            "none";

    }

}


/* =========================================================
   TOAST
========================================================= */

function showToast(title, message) {

    if (!toast) {
        return;
    }


    if (toastTitle) {
        toastTitle.textContent =
            title;
    }


    if (toastMessage) {
        toastMessage.textContent =
            message;
    }


    toast.style.display =
        "flex";


    clearTimeout(
        window.toastTimeout
    );


    window.toastTimeout =
        setTimeout(function () {

            hideToast();

        }, 4000);

}


function hideToast() {

    if (toast) {
        toast.style.display =
            "none";
    }

}


if (toastClose) {

    toastClose.addEventListener(
        "click",
        function () {

            hideToast();

        }
    );

}


/* =========================================================
   INITIAL STATE
========================================================= */

function initializeApp() {

    console.log(
        "[AI Legal Assistant] Initializing application..."
    );


    if (uploadButton) {
        uploadButton.disabled = true;
    }


    if (summaryButton) {
        summaryButton.disabled = true;
    }


    if (chatFeatureButton) {
        chatFeatureButton.disabled = true;
    }


    if (rightsButton) {
        rightsButton.disabled = true;
    }


    if (riskButton) {
        riskButton.disabled = true;
    }


    if (recommendationButton) {
        recommendationButton.disabled = true;
    }


    if (chatInput) {
        chatInput.disabled = true;
    }


    if (sendChatButton) {
        sendChatButton.disabled = true;
    }


    if (selectedFileBox) {
        selectedFileBox.style.display =
            "none";
    }


    if (documentInfo) {
        documentInfo.style.display =
            "none";
    }


    if (resultsSection) {
        resultsSection.style.display =
            "none";
    }


    if (loadingOverlay) {
        loadingOverlay.style.display =
            "none";
    }


    console.log(
        "[AI Legal Assistant] Initial state completed"
    );

}


initializeApp();


console.log(
    "[AI Legal Assistant] script.js initialization completed"
);
