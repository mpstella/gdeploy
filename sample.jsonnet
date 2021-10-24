local functionName = "hello-world";

{
  "name": functionName,
  "args": {
      "region": "australia-southeast1",
      "entry-point": "hello_http",
      "runtime": "python39",
      "update-labels": {
        "deployed_by": "gdeploy",
        "deployed_on": "yyyy-mm-dd"
      },
      "remove-labels": [
        "label1",
        "label2"
      ]
  },
  "flags": [
    "allow-unauthenticated",
    "trigger-http"
  ],
  "opts": ["alpha"]
}