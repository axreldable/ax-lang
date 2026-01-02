# Benchmark Results

## Benchmark results for `python`

| lang   | test_case    |   duration_sec |   pick_mem_mb | lang_version   |
|:-------|:-------------|---------------:|--------------:|:---------------|
| python | factorial    |      0.026897  |             0 | v1             |
| python | fibonacci    |      0.0261114 |             0 | v1             |
| python | higher_order |      0.0264599 |             0 | v1             |
| python | simple       |      0.0257928 |             0 | v1             |
| python | switch       |      0.0254359 |             0 | v1             |


## Benchmark results for `axlang`

| lang   | test_case    |   duration_sec |   pick_mem_mb | lang_version   |
|:-------|:-------------|---------------:|--------------:|:---------------|
| axlang | factorial    |       0.12076  |             0 | v1             |
| axlang | fibonacci    |       0.118396 |             0 | v1             |
| axlang | higher_order |       0.120332 |             0 | v1             |
| axlang | simple       |       0.115573 |             0 | v1             |
| axlang | switch       |       0.111555 |             0 | v1             |


## Benchmark aggregated `duration` results

| test_case    |   python_duration_sec |   axlang_duration_sec |
|:-------------|----------------------:|----------------------:|
| factorial    |             0.026897  |              0.12076  |
| fibonacci    |             0.0261114 |              0.118396 |
| higher_order |             0.0264599 |              0.120332 |
| simple       |             0.0257928 |              0.115573 |
| switch       |             0.0254359 |              0.111555 |


## Benchmark aggregated `memory` results

| test_case    |   python_pick_mem_mb |   axlang_pick_mem_mb |
|:-------------|---------------------:|---------------------:|
| factorial    |                    0 |                    0 |
| fibonacci    |                    0 |                    0 |
| higher_order |                    0 |                    0 |
| simple       |                    0 |                    0 |
| switch       |                    0 |                    0 |

