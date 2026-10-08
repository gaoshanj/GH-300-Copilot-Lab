# Business request

Add an endpoint that accepts a text payload and returns a deterministic checksum.

## Acceptance criteria

- `POST /checksum` accepts JSON with one required field: `text`.
- Empty text is rejected with HTTP 422.
- The response contains an integer field named `checksum`.
- The same input always produces the same output.
- Inputs are bounded to 10,000 characters.
- Add positive, negative, and boundary tests.

## Copilot exercise

Ask Copilot to propose a plan first. Then ask it to implement only the smallest change, show the diff, and run the tests. Compare the generated implementation with the acceptance criteria.

