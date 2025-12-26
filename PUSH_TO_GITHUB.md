# Commands to Push to GitHub

Run these commands in your terminal from the Portfolio directory:

```bash
cd /Users/princesslilith/Desktop/Portfolio

# Check git status
git status

# If not a git repo, initialize it:
git init
git remote add origin https://github.com/lilithfroude-ctrl/Portfolio.git
git branch -M main

# Stage all changes
git add .

# Commit changes
git commit -m "Add portfolio projects and resume"

# Push to main branch
git push -u origin main
```

If you encounter authentication issues, you may need to:
- Set up GitHub authentication (personal access token or SSH key)
- Or use: `git push -u origin main --force` (only if you're sure you want to overwrite remote)

