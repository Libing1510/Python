#include <tobii/tobii_licensing.h>
#include <tobii/tobii_config.h>
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <assert.h>
#include <string.h>
static size_t read_license_file(uint16_t *license)
{
    FILE *license_file = fopen("se_license_key_sample", "rb");
    if (!license_file)
    {
        printf("License key could not be found!\n");
        return 0;
    }
    fseek(license_file, 0, SEEK_END);
    long file_size = ftell(license_file);
    rewind(license_file);
    if (file_size <= 0)
    {
        fclose(license_file);
        printf("Unable to read License file!\n");
        return 0;
    }
    if (license)
    {
        size_t n = fread(license, sizeof(uint16_t), file_size / sizeof(uint16_t), license_file);
        assert(n > 0);
        (void)n;
    }
    fclose(license_file);
    return (size_t)file_size;
}
tobii_error_t create_device(tobii_api_t *api, tobii_device_t **device, char *url)
{
    tobii_error_t error;
    size_t license_size = read_license_file(0);
    assert(license_size > 0);
    uint16_t *license_key = (uint16_t *)malloc(license_size);
    memset(license_key, 0, license_size);
    read_license_file(license_key);
    tobii_license_key_t license = {license_key, license_size};
    tobii_license_validation_result_t license_result;
    error = tobii_device_create_ex(api, url, TOBII_FIELD_OF_USE_STORE_OR_TRANSFER_FALSE, &license, 1, &license_result,
                                   device);
    free(license_key);
    license_key = 0;
    if (error == TOBII_ERROR_CONNECTION_FAILED)
    {
        printf("Failed to connect to tracker.\n");
        Function
            Syntax
                Remarks
                    Return value return error;
    }
    return error;
}
tobii_error_t calibrate(tobii_device_t *device)
{
    tobii_error_t error = tobii_calibration_start(device, TOBII_ENABLED_EYE_BOTH);
    if (error != TOBII_ERROR_NO_ERROR)
    {
        return error;
    }
    printf("Look at the top left!\n");
    error = tobii_calibration_collect_data_2d(device, 0.1f, 0.1f);
    if (error != TOBII_ERROR_NO_ERROR)
    {
        return error;
    }
    printf("Look at the bottom right!\n");
    error = tobii_calibration_collect_data_2d(device, 0.9f, 0.9f);
    if (error != TOBII_ERROR_NO_ERROR)
    {
        return error;
    }
    printf("Look at the center!\n");
    error = tobii_calibration_collect_data_2d(device, 0.5f, 0.5f);
    if (error != TOBII_ERROR_NO_ERROR)
    {
        return error;
    }
    error = tobii_calibration_compute_and_apply(device);
    if (error != TOBII_ERROR_NO_ERROR)
    {
        return error;
    }
    return tobii_calibration_stop(device);
}
static void url_receiver(char const *url, void *user_data)
{
    char *buffer = (char *)user_data;
    if (*buffer != '\0')
        return; // only keep first value
    if (strlen(url) < 256)
        strcpy(buffer, url);
}
int main()
{
    tobii_api_t *api;
    tobii_error_t error = tobii_api_create(&api, NULL, NULL);
    assert(error == TOBII_ERROR_NO_ERROR);
    (void)error;
    char url[256] = {0};
    error = tobii_enumerate_local_device_urls(api, url_receiver, url);
    assert(error == TOBII_ERROR_NO_ERROR && *url != '\0');
    tobii_device_t *device;
    error = create_device(api, &device, url);
    if (error != TOBII_ERROR_NO_ERROR)
    {
        printf("Failed to create device!\n");
        tobii_api_destroy(api);
        return error;
    }
    error = calibrate(device);
    if (error == TOBII_ERROR_NO_ERROR)
    {
        printf("Calibration succeed!\n");
    }
    else
    {
        printf("Calibration failed!\n");
    }
    tobii_device_destroy(device);
    tobii_api_destroy(api);
    return 0;
}