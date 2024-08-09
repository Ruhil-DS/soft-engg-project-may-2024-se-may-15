<template>
    <button id="calculatorButton" type="button" class="btn btn-warning rounded-3 w-100" data-bs-toggle="modal" data-bs-target="#calculator">
                    <span class="fw-medium">Calculator <i class="bi bi-calculator-fill"></i></span>
    </button>
    <div class="modal fade" id="calculator" tabindex="-1" aria-labelledby="calculatorLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="calculatorLabel"><i class="bi bi-calculator"></i> Scientific Calculator</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <embed class="rounded-3 border" src="https://www.desmos.com/scientific" width="100%" height="400px" draggable></embed>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
#calculatorButton {
    font-size: 1.1rem;
}
</style>