# File Processor Skill

Process dropped files and extract relevant information.

## Metadata
- **Tier**: Bronze
- **Priority**: High
- **Dependencies**: Dashboard Updater, Task Manager
- **Triggers**: Files in /Needs_Action with type: file_drop

## Capabilities
- Read and analyze PDFs
- Parse CSV/Excel files
- Analyze images
- Extract text from documents
- Categorize file types
- Update Dashboard with findings

## Usage
```bash
/file-processor
```

## Expected Input
- File drop notifications in /Needs_Action
- Various file types (PDF, CSV, images, etc.)

## Expected Output
- Extracted information
- Categorized files in appropriate folders
- Dashboard updated
- Tasks created for follow-ups
