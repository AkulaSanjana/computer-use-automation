from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>LegacyBank Operations</title>
        </head>
        <body>
            <h1>LegacyBank Operations Console</h1>

            <form method="post" action="/search">
                <table>
                    <tr>
                        <td>Member Number</td>
                        <td>
                            <input type="text" name="member_id">
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                        <td>
                            <button type="submit">Search</button>
                        </td>
                    </tr>
                </table>
            </form>
        </body>
    </html>
    """


@app.post("/search", response_class=HTMLResponse)
def search(member_id: str = Form(...)):

    # Member 1
    if member_id == "12345":
        return """
        <html>
            <head>
                <title>Member Details</title>
            </head>
            <body>
                <h1>Member Details</h1>

                <table>
                    <tr>
                        <td>Name</td>
                        <td>Jane Doe</td>
                    </tr>
                    <tr>
                        <td>Member ID</td>
                        <td>12345</td>
                    </tr>
                    <tr>
                        <td>Savings Balance</td>
                        <td>$4280.12</td>
                    </tr>
                </table>

                <br>
                <a href="/">Back</a>
            </body>
        </html>
        """

    # Member 2
    if member_id == "67890":
        return """
        <html>
            <head>
                <title>Member Details</title>
            </head>
            <body>
                <h1>Member Details</h1>

                <table>
                    <tr>
                        <td>Name</td>
                        <td>John Smith</td>
                    </tr>
                    <tr>
                        <td>Member ID</td>
                        <td>67890</td>
                    </tr>
                    <tr>
                        <td>Savings Balance</td>
                        <td>$9150.75</td>
                    </tr>
                </table>

                <br>
                <a href="/">Back</a>
            </body>
        </html>
        """

    # Member not found
    return """
    <html>
        <head>
            <title>Member Not Found</title>
        </head>
        <body>
            <h1>Member Not Found</h1>
            <p>No member exists for the supplied ID.</p>
            <a href="/">Back</a>
        </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)