// Include Flatpickr Library
document.addEventListener("DOMContentLoaded", function () {
    const datePicker = document.getElementById("date-picker");

    // Initialize Flatpickr
    const flatpickrInstance = flatpickr(datePicker, {
        enable: [], // Will be updated dynamically
        dateFormat: "Y-m-d",
        disableMobile: true, // Ensures consistency across devices
        onChange: function () {
            document.getElementById("time-filter").value = "all"; // Reset time filter when date is selected
            updateTable();
        }
    });

    // Set default time filter and update the table on load
    document.getElementById("time-filter").value = "7d"; // Default selection
    updateTable(); // Load data initially
});

// Show loading animation
function showLoading() {
    document.getElementById("loading").style.display = "block";
    document.getElementById("table-container").style.display = "none";
}

// Hide loading animation
function hideLoading() {
    document.getElementById("loading").style.display = "none";
    document.getElementById("table-container").style.display = "block";
}

// Function to update table and populate Flatpickr
async function updateTable() {
    try {
        showLoading();  // Show loading animation

        const response = await fetch('/api/data_db');
        if (!response.ok) throw new Error("Network response was not ok");

        const textData = await response.text();
        let rows = textData.trim().split("\n").reverse(); // Latest records first

        let tableBody = document.getElementById("data-table-body");
        tableBody.innerHTML = ""; // Clear old data

        let availableDates = new Set();
        let availableDestinations = new Set(["All Destination", "Vessel 1", "Vessel 2"]); // Fixed destinations
        let now = new Date();
        let filteredRows = [];

        // Get selected filters
        const timeFilter = document.getElementById("time-filter").value || "7d";
        document.getElementById("time-filter").value = timeFilter; 

        const selectedDate = document.getElementById("date-picker").value;
        const selectedDestination = document.getElementById("destination-filter").value;

        rows.forEach(row => {
            let columns = row.split(",");
            let rowDate = columns[3]; // Date column
            let rowDestination = columns[6]; // Destination column
            let rowDateObj = new Date(rowDate);

            availableDates.add(rowDate); // Store unique dates

            let withinTimeFrame = false;
            if (timeFilter === "24h" && (now - rowDateObj) <= 86400000) {
                withinTimeFrame = true;
            } else if (timeFilter === "7d" && (now - rowDateObj) <= 604800000) {
                withinTimeFrame = true;
            } else if (timeFilter === "1m" && (now - rowDateObj) <= 2592000000) {
                withinTimeFrame = true;
            } else if (timeFilter === "all") {
                withinTimeFrame = true;
            }

            if (
                withinTimeFrame && 
                (!selectedDate || selectedDate === rowDate) && 
                (selectedDestination === "All Destination" || selectedDestination === rowDestination)
            ) {
                filteredRows.push(row);
            }
        });

        // Update Flatpickr with available dates
        let datePicker = document.getElementById("date-picker")._flatpickr;
        if (datePicker) {
            datePicker.set("enable", Array.from(availableDates)); // Allow only available dates
        }

        // Populate destination filter with available destinations
        let destinationFilter = document.getElementById("destination-filter");
        let currentSelection = destinationFilter.value;
        destinationFilter.innerHTML = ""; // Clear old options
        availableDestinations.forEach(dest => {
            let option = document.createElement("option");
            option.value = dest;
            option.textContent = dest;
            if (dest === currentSelection) {
                option.selected = true; // Maintain selection
            }
            destinationFilter.appendChild(option);
        });

        // Display data or show "No data available"
        if (filteredRows.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="8" style="text-align:center;">No data available</td></tr>`;
        } else {
            filteredRows.forEach(row => {
                let columns = row.split(",");
                let tableRow = `<tr>
                    <td>${columns[0]}</td>
                    <td>${columns[1]}</td>
                    <td>${columns[2]}</td>
                    <td>${columns[3]}</td>
                    <td>${columns[4]}</td>
                    <td>${columns[5]}</td>
                    <td>${columns[6]}</td>
                    <td>${columns[7]}</td>
                </tr>`;
                tableBody.innerHTML += tableRow;
            });
        }

    } catch (error) {
        console.error("Error fetching table data:", error);
    } finally {
        hideLoading(); // Hide loading animation
    }
}

// Event listeners to apply filters and reset conflicting filters
document.getElementById("time-filter").addEventListener("change", function () {
    document.getElementById("date-picker").value = ""; // Clear date when time filter is changed
    updateTable();
});

document.getElementById("destination-filter").addEventListener("change", updateTable);

// Update table every 30 seconds
setInterval(updateTable, 30000);
