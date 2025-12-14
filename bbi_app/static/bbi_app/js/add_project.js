document.addEventListener('DOMContentLoaded', function () {
  // --- Liczniki znaków ---
  function setupCharCounter(inputId, counterId, maxLength) {
    const input = document.getElementById(inputId);
    const counter = document.getElementById(counterId);
    
    if (input && counter) {
      counter.textContent = input.value.length;
      input.addEventListener('input', function() {
        counter.textContent = this.value.length;
      });
    }
  }
  
  setupCharCounter('id_title', 'title-counter', 40);
  setupCharCounter('id_organization_name', 'organization_name-counter', 40);
  setupCharCounter('id_description', 'description-counter', 500);
  setupCharCounter('id_contact_info', 'contact-counter', 100);
  
  // --- Dodawanie linków ---
  const addLinkBtn = document.getElementById('add-link-form');
  if (addLinkBtn) {
    const container = document.getElementById('link-form-container');
    const totalFormsInput = document.querySelector('input[name="links-TOTAL_FORMS"]');
    const formTemplate = `
      <div class="link-form flex flex-col md:flex-row items-center gap-2 mb-2">
        <input type="url" name="links-__prefix__-url" class="border-2 font-light border-black p-2 flex-1" placeholder="http://...">
        <input type="text" name="links-__prefix__-name" class="border-2 font-light border-black p-2 flex-1" placeholder="nazwij link">
      </div>
    `;

    addLinkBtn.addEventListener('click', function () {
      let formNum = parseInt(totalFormsInput.value);
      let newForm = formTemplate.replace(/__prefix__/g, formNum);
      container.insertAdjacentHTML('beforeend', newForm);
      totalFormsInput.value = formNum + 1;
    });
  }

  // --- Obsługa dodawania plików ---
  const addFileBtn = document.getElementById('add-file-form');
  if (addFileBtn) {
    const fileContainer = document.getElementById('file-form-container');
    const totalFileFormsInput = document.querySelector('input[name="files-TOTAL_FORMS"]');
    const MAX_FILES = 3;

    function updateFileButtonState() {
      const currentFiles = parseInt(totalFileFormsInput.value);
      if (currentFiles >= MAX_FILES) {
        addFileBtn.disabled = true;
        addFileBtn.classList.add('opacity-50', 'cursor-not-allowed');
      } else {
        addFileBtn.disabled = false;
        addFileBtn.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    }

    const fileFormTemplate = `
      <div class="file-form flex flex-col md:flex-row items-center gap-2 mb-2">
        <input type="file" name="files-__prefix__-file" class="border-2 border-black p-1.5 w-full md:w-1/2 font-light file:mr-2 file:py-1 file:px-2 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200">
        <input type="text" name="files-__prefix__-name" class="border-2 border-black p-2 w-full md:w-1/2 font-light" placeholder="nazwij plik">
      </div>
    `;

    addFileBtn.addEventListener('click', function () {
      let formNum = parseInt(totalFileFormsInput.value);
      if (formNum < MAX_FILES) {
        let newForm = fileFormTemplate.replace(/__prefix__/g, formNum);
        fileContainer.insertAdjacentHTML('beforeend', newForm);
        totalFileFormsInput.value = formNum + 1;
        updateFileButtonState();
      }
    });

    updateFileButtonState();
  }

  // --- Wybór finansowania ---
  const financingSelect = document.getElementById('id_financing_type');
  if (financingSelect) {
    const otherContainer = document.getElementById('financing_type_other_container');
    const otherInput = document.getElementById('id_financing_type_other');

    function toggleOtherFinancing() {
      if (financingSelect.value === 'other') {
        otherContainer.classList.remove('hidden');
        otherInput.required = true;
      } else {
        otherContainer.classList.add('hidden');
        otherInput.required = false;
        otherInput.value = '';
      }
    }

    financingSelect.addEventListener('change', toggleOtherFinancing);
    toggleOtherFinancing(); // Sprawdź stan początkowy
  }

  // --- Podgląd zdjęć i walidacja ---
  document.querySelectorAll('input.upload-input').forEach((input) => {
    const MAX_IMAGE_SIZE_MB = 4;
    const MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024;

    input.addEventListener('change', async () => {
      const label = document.querySelector(`label[for="${input.id}"]`);
      if (!label) return;
      const placeholder = label.querySelector('.placeholder');
      const preview = label.querySelector('img.preview');
      const parentContainer = input.parentElement;

      const existingError = parentContainer.querySelector('.size-error-message');
      if (existingError) {
        existingError.remove();
      }

      if (input.files && input.files[0]) {
        const file = input.files[0];

        if (file.size > MAX_IMAGE_SIZE_BYTES) {
          const errorDiv = document.createElement('div');
          errorDiv.className = 'text-red-500 text-sm mt-1 size-error-message';
          errorDiv.innerHTML = `<p>Plik jest za duży. Maksymalny rozmiar to ${MAX_IMAGE_SIZE_MB} MB.</p>`;
          parentContainer.appendChild(errorDiv);
          input.value = '';
          preview.src = '';
          preview.classList.add('hidden');
          placeholder.classList.remove('hidden');
          return;
        }

        if (file.name.toLowerCase().endsWith('.heic') || file.name.toLowerCase().endsWith('.heif')) {
          try {
            if (typeof heic2any !== 'undefined') {
              const convertedBlob = await heic2any({ blob: file, toType: 'image/jpeg', quality: 0.8 });
              preview.src = URL.createObjectURL(convertedBlob);
            } else {
              console.warn('Biblioteka heic2any nie jest załadowana.');
            }
          } catch (error) {
            console.error('Błąd konwersji HEIC:', error);
          }
        } else {
          preview.src = URL.createObjectURL(file);
        }

        preview.classList.remove('hidden');
        placeholder.classList.add('hidden');
      } else {
        preview.src = '';
        preview.classList.add('hidden');
        placeholder.classList.remove('hidden');
      }
    });
  });

  // --- Obsługa licznika tagów ---
  const checkboxes = document.querySelectorAll('.tag-checkbox');
  if (checkboxes.length > 0) {
    const counter = document.getElementById('selected-count');
    const MAX_TAGS = 5;

    function updateCounter() {
      const checkedCount = document.querySelectorAll('.tag-checkbox:checked').length;
      counter.textContent = checkedCount;

      const limitReached = checkedCount >= MAX_TAGS;
      checkboxes.forEach(checkbox => {
        if (!checkbox.checked) {
          checkbox.disabled = limitReached;
          checkbox.parentElement.querySelector('label').classList.toggle('opacity-50', limitReached);
          checkbox.parentElement.querySelector('label').classList.toggle('cursor-not-allowed', limitReached);
        }
      });
    }

    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', updateCounter);
    });

    updateCounter();
  }
});