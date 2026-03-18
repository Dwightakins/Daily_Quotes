# Daily Quote Automation

This project gives you a simple automation and a small website.

Every day, GitHub can run a Python script that picks a quote and updates:

- a website page,
- a JSON data file,
- a quote history file.

## What GitHub Is Doing For You

GitHub Actions is the automation tool here.

It does this automatically:

1. opens your repository on GitHub,
2. runs the Python script,
3. saves the newest quote,
4. updates the files in your repository.

That means you do not have to manually change the quote every day.

## What You Can View

This project includes a simple webpage in `docs/index.html`.

After you push the repo to GitHub and turn on GitHub Pages, you will be able to open a public link like:

`https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`

That page will show the latest daily quote.

## Files You Should Know

- `scripts/generate_quote.py` picks the quote and writes the updated files.
- `.github/workflows/daily-quote.yml` tells GitHub when to run the automation.
- `docs/index.html` is the website page.
- `docs/latest-quote.json` stores the newest quote for the page.
- `quotes-history.md` keeps a record of past quotes.

## Project Structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- daily-quote.yml
|-- docs/
|   |-- index.html
|   `-- latest-quote.json
|-- scripts/
|   `-- generate_quote.py
|-- .gitignore
|-- quotes-history.md
`-- README.md
```

## How To Put It On GitHub

1. Create a new empty repository on GitHub.
2. Upload these files, or use Git commands to push them.
3. Open the `Actions` tab and run `Daily Quote Automation` once.
4. Open the repository `Settings`.
5. Find `Pages`.
6. Set the source to `Deploy from a branch`.
7. Choose the `main` branch and the `/docs` folder.
8. Save it.

After that, GitHub will give you a website link for your quote page.

## Git Commands To Push It

```powershell
git add .
git commit -m "Add daily quote automation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

## How To Change The Quotes Later

Open `scripts/generate_quote.py` and edit the `QUOTES` list.

You can replace the quote text and author names with your own favorites.

## Beginner Explanation

Think of the project like this:

- the Python file chooses the quote,
- GitHub runs it every day,
- the website shows the result.
