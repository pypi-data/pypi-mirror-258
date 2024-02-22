# AWS Daily CloudWatch Logs Archiver

[![GitHub](https://img.shields.io/github/license/gammarer/aws-daily-cloud-watch-logs-archiver?style=flat-square)](https://github.com/gammarer/aws-daily-cloud-watch-logs-archiver/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-daily-cloud-watch-logs-archiver?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-daily-cloud-watch-logs-archiver)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-daily-cloud-watch-logs-archiver?style=flat-square)](https://pypi.org/project/gammarer.aws-daily-cloud-watch-logs-archiver/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.DailyCloudWatchLogsArchiver?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.DailyCloudWatchLogsArchiver/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-daily-cloud-watch-logs-archiver?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-daily-cloud-watch-logs-archiver/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarer/aws-daily-cloud-watch-logs-archiver/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarer/aws-daily-cloud-watch-logs-archiver/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarer/aws-daily-cloud-watch-logs-archiver?sort=semver&style=flat-square)](https://github.com/gammarer/aws-daily-cloud-watch-logs-archiver/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarer/aws-daily-cloud-watch-logs-archiver)](https://constructs.dev/packages/@gammarer/aws-daily-cloud-watch-logs-archiver)

AWS CloudWatch Logs daily(13:00Z) archive to s3 bucket.

## Resources

This construct creating resource list.

* S3 Bucket (log-archive-xxxxxxxx from @gammarer/aws-secure-log-bucket)
* Lambda function execution role
* Lambda function
* Lambda function log group
* StepFunctions state machine execution role
* StepFunctions state machine
* EventBridge Scheduler execution role
* EventBridge Scheduler

## Architecture

![architecture](/architecture.drawio.svg)

## Install

### TypeScript

```shell
npm install @gammarer/aws-daily-cloud-watch-logs-archiver
# or
yarn add @gammarer/aws-daily-cloud-watch-logs-archiver
```

### Python

```shell
pip install gammarer.aws-daily-cloud-watch-logs-archiver
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.DailyCloudWatchLogsArchiver
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-daily-cloud-watch-logs-archiver</artifactId>
</dependency>
```

## Example

```shell
npm install @gammarer/aws-daily-cloud-watch-logs-archiver
```

```python
import { DailyCloudWatchLogsArchiver } from '@gammarer/aws-daily-cloud-watch-logs-archiver';

new DailyCloudWatchLogsArchiver(stack, 'DailyCloudWatchLogsArchiver', {
    resource: {
      key: 'DailyLogExport',
      values: ['Yes'],
    },
});
```

## Otherwise

If you want to export old log files, please refer to the following repository. The log file will be exported in the same output format.

[AWS CloudWatch Logs Exporter](https://github.com/gammarer/aws-cloud-watch-logs-exporter)

## License

This project is licensed under the Apache-2.0 License.
