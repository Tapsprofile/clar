namespace VirtualTryOn.Api.Models;

public sealed record TryOnResponse(
    string jobId,
    string resultUrl
);

