# Building Go Projects

This monorepo contains multiple Go modules located in the `go/` directory.

## Project Structure

- `go/libs/`: Shared libraries
- `go/apps/`: Applications / Services
- `go/lambdas/`: AWS Lambda functions

## Prerequisites

- Go 1.21 or later

## Building Components

Navigate to the specific component directory to build it.

### Common Utils

```bash
cd go/libs/common-utils
go mod tidy
go build ./...
```

### Processor App

```bash
cd go/apps/processor
go mod tidy
go build ./...
```

### Notifier Lambda

```bash
cd go/lambdas/notifier
go mod tidy
go build ./...
```

## Testing

To run tests for a specific module:

```bash
go test ./...
```
