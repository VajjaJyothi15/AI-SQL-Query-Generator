function copySQL() {

    const sqlText =
        document.getElementById("sqlQuery").innerText;

    navigator.clipboard.writeText(sqlText);

    alert("SQL Query Copied!");
}