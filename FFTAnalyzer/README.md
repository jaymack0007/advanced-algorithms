# FFTAnalyzer



Week 12 project for CSC5300 Advanced Algorithms.



`FFTAnalyzer` is a numerical computing toolkit that implements matrix algorithms, Fast Fourier Transform algorithms, signal processing, image processing, audio processing, time-series analysis, visualization, and numerical stability tools.



## Features



### Core Numerical Algorithms



- Classical O(n³) matrix multiplication

- LUP decomposition with partial pivoting

- Forward and back substitution

- Linear-system solving

- Determinant calculation

- Householder QR decomposition

- Power iteration

- Matrix and vector norms

- Condition-number estimation

- Residual and numerical error calculations

- Catastrophic cancellation demonstration



### Fast Fourier Transform



- Recursive radix-2 FFT

- Iterative radix-2 FFT

- Bit-reversal permutation

- Inverse FFT

- Direct DFT reference implementation

- Circular convolution

- Linear convolution

- Power-of-two utilities



### Signal Processing



Signal generators:



- Sine wave

- Multi-tone signal

- Linear chirp

- White noise

- Pink noise



Filters and windows:



- Low-pass filter

- High-pass filter

- Band-pass filter

- Hann window

- Hamming window

- Blackman window



Analysis:



- Periodogram

- Power spectral density

- Peak-frequency detection

- Dominant-frequency detection

- STFT spectrogram



### Image Processing



FFT-based image tools:



- 2D FFT and inverse FFT

- Gaussian blur

- Sobel edge detection

- Laplacian edge detection

- Frequency-domain denoising

- Image sharpening

- Frequency-magnitude visualization



Compression tools:



- 2D DCT and inverse DCT

- JPEG-style quantization

- Block-based image compression

- Image reconstruction

- Mean squared error

- Peak signal-to-noise ratio

- Zero-coefficient measurement



### Applications



Audio processing:



- WAV loading and saving

- Frequency-domain audio filters

- Audio analysis

- Spectrogram generation

- WAV processing workflow



Image processing:



- Image loading and saving

- Filter selection

- Frequency visualization

- Image compression

- Compression quality metrics



Time-series analysis:



- Moving average

- FFT-based autocorrelation

- Periodicity detection

- Dominant-period estimation

- Seasonality measurement



### Visualization



- FFT spectrum plots

- Spectrograms

- 2D FFT heatmaps

- Condition-number plots

- Signal comparison plots

- FFT construction animation

- Frequency-filter animation



## Project Structure



```text

FFTAnalyzer/

|

+-- fft\_analyzer/

|   +-- applications/

|   |   +-- audio\_processor.py

|   |   +-- data\_analyzer.py

|   |   +-- image\_processor.py

|   |

|   +-- core/

|   |   +-- fft.py

|   |   +-- matrix.py

|   |   +-- numerical.py

|   |

|   +-- image/

|   |   +-- compression.py

|   |   +-- filters.py

|   |

|   +-- signal/

|   |   +-- analysis.py

|   |   +-- filters.py

|   |   +-- generators.py

|   |

|   +-- visualization/

|       +-- animations.py

|       +-- plots.py

|

+-- benchmarks/

|   +-- benchmark\_fft.py

|   +-- benchmark\_matrix.py

|   +-- benchmark\_numerical.py

|   +-- smoke\_fft.py

|

+-- docs/

|   +-- chapter12\_report.md

|

+-- examples/

|   +-- audio\_demo.py

|   +-- image\_demo.py

|   +-- signal\_demo.py

|

+-- results/

+-- tests/

+-- README.md

+-- setup.py

```



## Setup



The project was developed with Python 3.14.5.



From the repository root, activate the existing virtual environment:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Install the repository requirements if needed:



```powershell

python -m pip install -r requirements.txt

```



The Week 12 package can also be installed from its project directory:



```powershell

cd .\\FFTAnalyzer

python -m pip install .

cd ..

```



## Run Week 12 Tests



From the repository root:



```powershell

python -m pytest .\\FFTAnalyzer\\tests -q

```



The completed Week 12 test suite contains 360 passing tests.



A Matplotlib warning may appear when animation objects are created during testing without being displayed or saved. This warning does not indicate a test failure.



## Run the Examples



Signal-processing demo:



```powershell

python -m FFTAnalyzer.examples.signal\_demo

```



Audio-processing demo:



```powershell

python -m FFTAnalyzer.examples.audio\_demo

```



Image-processing demo:



```powershell

python -m FFTAnalyzer.examples.image\_demo

```



Generated images and WAV files are stored in:



```text

FFTAnalyzer/results/

```



## FFT Benchmarks



Run the FFT benchmark:



```powershell

python -m FFTAnalyzer.benchmarks.benchmark\_fft

```



Run the large-input smoke benchmark:



```powershell

python -m FFTAnalyzer.benchmarks.smoke\_fft

```



The iterative FFT successfully processed 1,048,576 values in 2.214148 seconds during the official benchmark. Maximum error compared with NumPy was 4.479e-12.



The direct DFT versus iterative FFT benchmark also demonstrated the expected complexity difference. At n=512:



```text

Direct DFT:     0.158948 seconds

Iterative FFT:  0.000188 seconds

Speedup:        844.71x

```



## Numerical Benchmarks



Run the numerical benchmark:



```powershell

python -m FFTAnalyzer.benchmarks.benchmark\_numerical

```



Run the stabilized matrix benchmark:



```powershell

python -m FFTAnalyzer.benchmarks.benchmark\_matrix

```



The classical matrix multiplication implementation produced numerical differences from NumPy on the order of 10^-14 while showing the expected increase in runtime as matrix size increased.



The conditioning experiment demonstrates how matrices become increasingly sensitive as their rows approach linear dependence. The tested matrix crossed the project's ill-conditioned threshold when its condition number reached approximately 4.0e11.



## Image Compression Results



The DCT compression benchmark tested quality settings from 10 through 90.



At quality 10:



```text

PSNR:              32.467 dB

Zero coefficients: 97.357%

```



At quality 90:



```text

PSNR:              42.663 dB

Zero coefficients: 82.556%

```



The results demonstrate the expected tradeoff between aggressive coefficient reduction and reconstruction quality.



## Result Files



Benchmark outputs include:



```text

compression\_quality.png

compression\_results.csv

conditioning\_results.csv

dft\_vs\_fft.png

dft\_vs\_fft\_results.csv

fft\_benchmark\_results.csv

fft\_runtime\_scaling.png

matrix\_benchmark\_results.csv

matrix\_conditioning.png

matrix\_runtime.png

```



The examples also generate signal, audio, and image demonstration outputs in the same results directory.



## Technical Report



The Week 12 technical report is located at:



```text

FFTAnalyzer/docs/chapter12\_report.md

```



The report covers:



- Matrix and numerical algorithms

- Numerical stability and conditioning

- Recursive and iterative FFT

- Direct DFT versus FFT performance

- Signal and audio processing

- Image filtering and DCT compression

- Benchmark results and complexity analysis
